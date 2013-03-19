from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from bitcoin_eshop.settings import MASTER_PUBLIC_KEY
from web.models import Products, ProductForm, ContactInformationForm, Order
from web.open_wallet import *

def index(request):
	if request.method == 'POST':
		forms = []
		for product in Products().all:
			if request.POST['product'] == product:
				form = ProductForm(request.POST)
				if form.is_valid():
					return HttpResponseRedirect('/order/?product=' + form.cleaned_data['product'] + '&count=' + str(form.cleaned_data['count']))
			else:
				form = ProductForm()
			form.set_product(product)
			forms.append(form)
	else:
		forms = []
		for product in Products().all:
			form = ProductForm()
			form.set_product(product)
			forms.append(form)

	return render(request, 'web/index.html', {
		'forms': forms,
	})

def order(request):
	if request.method == 'POST':
		product = request.POST['product']
		count = request.POST['count']
		form = ContactInformationForm(request.POST)
		if form.is_valid():

			# address generator
			w = get_wallet_or_create(MASTER_PUBLIC_KEY)
			a = get_new_address(MASTER_PUBLIC_KEY)
			validate_address_format(a)
			a = get_new_address(MASTER_PUBLIC_KEY)
			validate_address_format(a)
			a = get_new_address(MASTER_PUBLIC_KEY)
			validate_address_format(a)

			# TODO:
			# make address list storage
			# generate address and QR code
			# save data
			# send emails
			# print address and QR code
			return HttpResponseRedirect('/checkout/')
	else:
		try:
			product = request.GET['product']
			count = request.GET['count']
			validate = ProductForm({'product': product, 'count': count})
			if validate.is_valid():
				form = ContactInformationForm(initial={'product': product, 'count': count})
			else:
				return HttpResponseRedirect('/')
		except Exception, e:
			return HttpResponseRedirect('/')

	return render(request, 'web/order.html', {
		'product': product,
		'count': count,
		'form': form,
	})

def checkout(request):
	return render(request, 'web/checkout.html', {})

def add(request):
	# add new order into database
	newOrder = Order(
		wallet_address = '12345address',
		product = 'chleba',
		count = 2,
		customer = 'Pepa Novak',
		email = 'pepa@example.com',
		customer_address = 'Zelena 4, 29000 Praha 6',
	)

	newOrder.save()

	return render(request, 'web/add.html', {'orders': Order.objects.all()})