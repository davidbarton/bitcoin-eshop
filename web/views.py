from django.shortcuts import render, get_object_or_404
from web.models import Order

def index(request):
    # now return the rendered template
    return render(request, 'web/index.html', {})