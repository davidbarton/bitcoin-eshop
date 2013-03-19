from django.shortcuts import render, get_object_or_404
from web.models import Order
from web.open_wallet import *

def index(request):
    # now return the rendered template
    master_public_key_hex = "112cee2e893f9e2531b15f013b05a921b917933a310191122470661995e9083ad873e574929a982e142fb3c3c1c3c38a98894802feef7b1c177cc3970cbf708b"
    w = get_wallet_or_create(master_public_key_hex)
    a = get_new_address(master_public_key_hex)
    validate_address_format(a)
    a = get_new_address(master_public_key_hex)
    validate_address_format(a)
    a = get_new_address(master_public_key_hex)
    validate_address_format(a)
    a = get_new_address(master_public_key_hex)
    validate_address_format(a)
    return render(request, 'web/index.html', {'msg': a})

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