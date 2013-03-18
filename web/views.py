from django.shortcuts import render, get_object_or_404
from web.models import Order

def index(request):
    # now return the rendered template
    return render(request, 'web/index.html', {})

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