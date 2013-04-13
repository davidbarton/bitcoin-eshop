# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.signing import TimestampSigner
from django.core import signing, mail
from django.contrib.auth import authenticate, login

from datetime import datetime, timedelta
from decimal import Decimal
from math import ceil
import json
import urllib

import mexbtcapi
from mexbtcapi.concepts.currencies import EUR, BTC
from mexbtcapi.concepts.currency import Amount

import requests

from web.models import MasterPublicKeys, Products, Orders
from web.forms import ProductForm, ContactInformationForm
from web.open_wallet import get_wallet_or_create, get_new_address

currency = EUR
raw_shipping_fee = 1.2
url_secret = "fnfDHUKFW8hFff54"

signer = TimestampSigner()

def index(request):

	exchange_rate = get_exchange_rate()
	
	products_out = []
	price_list = {}

	for product in Products.objects.all():
		if request.method == 'POST' and request.POST['product'] == product.title:
			form = ProductForm(request.POST)

			# build second (address) form
			if form.is_valid():
				product_title = request.POST['product']
				count = request.POST['count']

				# get fixed price list for all goods (or calc new one) and calculate order price
				try:
					price_list = json.loads(signer.unsign(request.session.get('price_list', False), max_age = 60 * 5))
					price = calculate_order_price(price_list[str(product.id)], count, price_list['shipping_fee'])
					price_update = False
				except (signing.BadSignature, KeyError):
					print("Tampering detected! Price has been updated!")
					price = calculate_order_price(get_exchange_value(exchange_rate, product.base_price), count, get_exchange_value(exchange_rate, raw_shipping_fee))
					price_update = True

				# fix order price
				try:
					del request.session['price_fixed']
				except KeyError:
					pass
				request.session['price_fixed'] = signer.sign(json.dumps({product.id:str(price)}))

				# render second (address) form
				form = ContactInformationForm(initial={'product': product_title, 'count': count})
				return render(request, 'web/order.html', {
					'product_title': product_title,
					'count': count,
					'price': price,
					'price_update': price_update,
					'form': form
				})
		else:
			form = ProductForm()

		# build simple form for each product and calc their prices
		form.set_product(product.title)
		price = get_exchange_value(exchange_rate, product.base_price)
		price_list[product.id] = str(price)
		products_out.append({
			'title': product.title,
			'price': price,
			'img': product.img,
			'form': form
		})

	# fix price list (all goods)
	shipping_fee = get_exchange_value(exchange_rate, raw_shipping_fee)
	price_list["shipping_fee"] = str(shipping_fee)
	request = fix_price_list(request, price_list)

	msg_old_price = check_msg_old_price(request)
	
	return render(request, 'web/index.html', {
		'products': products_out,
		'shipping_fee': shipping_fee,
		'msg_old_price': msg_old_price
	})

def order(request):
	# render finished order detail
	if request.method == 'GET':
		try:
			order = Orders.objects.get(id=url_hash_to_order_id(request.GET['o']))
		except KeyError:
			return HttpResponseRedirect('/')

		qr_url = 'https://chart.googleapis.com/chart?chs=250x250&cht=qr&chl=' + order.wallet_address

		return render(request, 'web/checkout.html', {
			'order': order,
			'qrcode': qr_url
		})

	product_title = request.POST['product']
	count = request.POST['count']
	product = Products.objects.get(title=product_title)
	form = ContactInformationForm(request.POST)
	if form.is_valid():
		try:
			# load fixed price
			price_fixed = json.loads(signer.unsign(request.session.get('price_fixed', False), max_age = 60 * 15))
			try:
				price = price_fixed[str(product.id)]
			except KeyError:
				return HttpResponseRedirect('/')

			# get wallet address
			mpk_row = product.master_public_key
			mpk_products = Products.objects.filter(master_public_key=mpk_row)
			nth_address = 0
			for mpk_product in mpk_products:
				nth_address += len(Orders.objects.filter(product=mpk_product))
			wallet = get_wallet_or_create(mpk_row.master_public_key)
			wallet_address = get_new_address(mpk_row.master_public_key, nth_address)

			# build order object
			order = Orders(
				wallet_address = wallet_address,
				price = price,
				product = product,
				count = request.POST['count'],
				email = request.POST['email'],
				name = request.POST['name'],
				address = request.POST['address'],
				city = request.POST['city'],
				postcode = request.POST['postcode']
			)
			order.save()

			send_finished_order_email(order)
			return HttpResponseRedirect('/order?o=' + order_id_to_url_hash(order.id))

		# deteced old price, redirect to get new one
		except (signing.BadSignature, KeyError):
			print("Tampering detected! Reditect to home and display old price message.")
			return HttpResponseRedirect('/?msg=old-price')
	else:
		# validate fixed order price (or calc new one)
		try:
			price_fixed = json.loads(signer.unsign(request.session.get('price_fixed', False), max_age = 60 * 10))
			try:
				price = price_fixed[str(product.id)]
			except KeyError:
				return HttpResponseRedirect('/')
			price_update = False
		except (signing.BadSignature, KeyError):
			print("Tampering detected! Price has been updated!")
			exchange_rate = get_exchange_rate()
			price = calculate_order_price(get_exchange_value(exchange_rate, product.base_price), count, get_exchange_value(exchange_rate, raw_shipping_fee))
			price_update = True

			try:
				del request.session['price_fixed']
			except KeyError:
				pass

			request.session['price_fixed'] = signer.sign(json.dumps({product.id:str(price)}))

		# render invalid second (address) form
		return render(request, 'web/order.html', {
			'product_title': product_title,
			'count': count,
			'price': price,
			'price_update': price_update,
			'form': form
		})

def update(request):
	count_accepted = 0
	count_canceled = 0
	orders = Orders.objects.filter(transaction_status=0)

	for order in orders:
		if order.created <= (datetime.now() - timedelta(days = 2)):
			order.transaction_status = 2
			order.save()
			send_canceled_order_email(order)
			count_canceled += 1
		else:
			url = "http://blockchain.info/q/addressbalance/" + order.wallet_address + "?confirmations=6"
			r = requests.get(url)
			num = Decimal(r.text) / 100000000
			if num >= order.price:
				order.transaction_status = 1
				order.save()
				send_accepted_order_email(order)
				count_accepted += 1

	count_orders = len(orders)
	count_unchanged = count_orders - count_accepted - count_canceled
	print "orders: " + str(count_orders) + ", accepted: " + str(count_accepted) + ", canceled: " + str(count_canceled) + ", unchanged: " + str(count_unchanged)
	
	if request.user.is_authenticated():
		return render(request, 'web/list.html', { 'orders': orders })
	else:
		return HttpResponseRedirect('/admin')

def list_all(request):
	if request.user.is_authenticated():
		orders = Orders.objects.all()
		return render(request, 'web/list.html', { 'orders': orders })
	else:
		return HttpResponseRedirect('/admin')

def order_id_to_url_hash(order_id):
	return urllib.quote((url_secret + str(order_id)).encode('base64','strict'))

def url_hash_to_order_id(url_hash):
	return urllib.unquote(url_hash.decode('base64','strict')).replace(url_secret, "")

def get_exchange_rate():
	mtgox_api = mexbtcapi.apis[0]
	return mtgox_api.market(currency).getTicker().sell

def get_exchange_value(exchange_rate, base_price):
	value = exchange_rate.convert(Amount(base_price, currency)).value
	return ceil(value * 100000) / 100000

def check_msg_old_price(request):
	try:
		msg = request.GET['msg']
		return True
	except KeyError:
		return False

def calculate_order_price(product_price, count, shipping_fee):
	price = Decimal(product_price) * Decimal(count) + Decimal(shipping_fee)
	return ceil(price * 100000) / 100000

def fix_price_list(request, price_list):
	try:
		del request.session['price_list']
	except KeyError:
		pass

	request.session['price_list'] = signer.sign(json.dumps(price_list))
	return request

def send_finished_order_email(order):
	subject = '[Potvrzení objednávky] Binary Logic Management LLC'
	body = 'Hello world...'
	my_send_email(subject, body, order.email)

def send_accepted_order_email(order):
	subject = '[Platba přijata] Binary Logic Management LLC'
	body = 'Hello world...'
	my_send_email(subject, body, order.email)

def send_canceled_order_email(order):
	subject = '[Objednávka zrušena] Binary Logic Management LLC'
	body = 'Hello world...'
	my_send_email(subject, body, order.email)

def my_send_email(subject, body, customer_mail):
	from_mail = 'btceshop@gmail.com'
	email = mail.EmailMessage(subject, body, from_mail, [customer_mail], [from_mail])
	try:
		email.send(fail_silently=False)
	except Exception:
		print "Email send failed"