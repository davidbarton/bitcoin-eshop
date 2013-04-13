from django.contrib import admin
from web.models import MasterPublicKeys, Products, Variables

admin.site.register(MasterPublicKeys)
admin.site.register(Products)
admin.site.register(Variables)