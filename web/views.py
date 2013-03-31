from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.signing import TimestampSigner
from django.core import signing

from decimal import Decimal
import json

import mexbtcapi
from mexbtcapi.concepts.currencies import EUR, BTC
from mexbtcapi.concepts.currency import Amount

from web.models import *
from web.open_wallet import *

signer = TimestampSigner()

def index(request):
	exchange_rate = get_exchange_rate()
	
	products_out = []
	price_list = {}

	for product in Products.objects.all():
		if request.method == 'POST' and request.POST['product'] == product.title:
			form = ProductForm(request.POST)
			if form.is_valid():
				product_title = request.POST['product']
				count = request.POST['count']

				try:
					price_list = json.loads(signer.unsign(request.session.get('price_list', False), max_age = 60 * 5))
					price = Amount(Decimal(price_list[str(product.id)]) * Decimal(count), BTC)
					price_update = False
				except (signing.BadSignature, KeyError):
					print("Tampering detected! Price has been updated!")
					price = Amount(Decimal(get_exchange_value(exchange_rate, product.base_price).value) * Decimal(count), BTC)
					price_update = True

				try:
					del request.session['price_fixed']
				except KeyError:
					pass

				request.session['price_fixed'] = signer.sign(json.dumps({product.id:str(price.value)}))

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
		form.set_product(product.title)
		price = get_exchange_value(exchange_rate, product.base_price)
		price_list[product.id] = str(price.value)
		products_out.append({
			'title': product.title,
			'price': price,
			'img': product.img,
			'form': form
		})

	try:
		del request.session['price_list']
	except KeyError:
		pass

	request.session['price_list'] = signer.sign(json.dumps(price_list))
	
	try:
		q = request.GET['msg']
		msg_old_price = True
	except KeyError:
		msg_old_price = False
	
	return render(request, 'web/index.html', {
		'products': products_out,
		'msg_old_price': msg_old_price
	})

def order(request):
	if request.method != 'POST':
		return HttpResponseRedirect('/')

	product_title = request.POST['product']
	count = request.POST['count']
	product = Products.objects.get(title=product_title)
	form = ContactInformationForm(request.POST)
	if form.is_valid():
		try:
			price_fixed = json.loads(signer.unsign(request.session.get('price_fixed', False), max_age = 60 * 15))
			try:
				price = price_fixed[str(product.id)]
			except KeyError:
				return HttpResponseRedirect('/')

			mpk_row = product.master_public_key
			mpk_products = Products.objects.filter(master_public_key=mpk_row)
			nth_address = 0
			for mpk_product in mpk_products:
				nth_address += len(Orders.objects.filter(product=mpk_product))
			mpk = mpk_row.master_public_key

			wallet = get_wallet_or_create(mpk)
			wallet_address = get_new_address(mpk, nth_address)

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

			qr_url = 'https://chart.googleapis.com/chart?chs=250x250&cht=qr&chl=' + wallet_address

			return render(request, 'web/checkout.html', {
				'order': order,
				'price': Amount(price, BTC),
				'qrcode': qr_url
			})
		except (signing.BadSignature, KeyError):
			print("Tampering detected! Reditect to home and display old price message.")
			return HttpResponseRedirect('/?msg=old-price')
	else:
		try:
			price_fixed = json.loads(signer.unsign(request.session.get('price_fixed', False), max_age = 60 * 10))
			try:
				price = Amount(price_fixed[str(product.id)], BTC)
			except KeyError:
				return HttpResponseRedirect('/')
			price_update = False
		except (signing.BadSignature, KeyError):
			print("Tampering detected! Price has been updated!")
			price = Amount(Decimal(get_exchange_value(get_exchange_rate(), product.base_price).value) * Decimal(count), BTC)
			price_update = True

			try:
				del request.session['price_fixed']
			except KeyError:
				pass

			request.session['price_fixed'] = signer.sign(json.dumps({product.id:str(price.value)}))

		return render(request, 'web/order.html', {
			'product_title': product_title,
			'count': count,
			'price': price,
			'price_update': price_update,
			'form': form,
		})

def get_exchange_rate():
	mtgox_api = mexbtcapi.apis[0]
	return mtgox_api.market(EUR).getTicker().sell

def get_exchange_value(exchange_rate, base_price):
	return exchange_rate.convert(Amount(base_price, EUR))