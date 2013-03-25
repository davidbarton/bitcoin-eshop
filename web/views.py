from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from web.models import *
from web.open_wallet import *

def index(request):
	if request.method == 'POST':
		forms = []
		for product in Products.objects.all():
			if request.POST['product'] == product.title:
				form = ProductForm(request.POST)
				if form.is_valid():
					product = request.POST['product']
					count = request.POST['count']
					form = ContactInformationForm(initial={'product': product, 'count': count})
					return render(request, 'web/order.html', {
						'product': product,
						'count': count,
						'form': form
					})
			else:
				form = ProductForm()
			form.set_product(product)
			forms.append(form)
	else:
		forms = []
		for product in Products.objects.all():
			form = ProductForm()
			form.set_product(product.title)
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
			product_row = Products.objects.get(title=product)
			mpk_row = product_row.master_public_key
			mpk_products = Products.objects.filter(master_public_key=mpk_row)
			nth_adress = len(Orders.objects.filter(product=mpk_products))
			mpk = mpk_row.master_public_key

			wallet = get_wallet_or_create(mpk)
			wallet_address = get_new_address(mpk, nth_adress)

			order = Orders(
				wallet_address = wallet_address,
				price = '1',
				product = product_row,
				count = request.POST['count'],
				email = request.POST['email'],
				name = request.POST['name'],
				address = request.POST['address'],
				city = request.POST['city'],
				postcode = request.POST['postcode']
			)
			order.save()

			# https://google-developers.appspot.com/chart/infographics/docs/overview

			return render(request, 'web/checkout.html', {
				'order': order
			})
		else:
			return render(request, 'web/order.html', {
				'product': product,
				'count': count,
				'form': form,
			})
	else:
		return HttpResponseRedirect('/')