from django.db import models
from django import forms

class Products:
	def __init__(self):
		self.all = ['chleba', 'pastika', 'pivo']

class ProductForm(forms.Form):
	product = forms.CharField(
		widget = forms.HiddenInput(),
		initial = ''
	)
	count = forms.IntegerField(
		max_value = 99,
		min_value = 1,
		label = '',
		initial = 1
	)
	def set_product(self, product):
		self.fields['product'].initial = product
		self.fields['count'].label = product

class ContactInformationForm(forms.Form):
	product = forms.CharField(widget=forms.HiddenInput())
	count = forms.IntegerField(widget=forms.HiddenInput())
	customer = forms.CharField(max_length=60)
	email = forms.EmailField(max_length=80)
	customer_address = forms.RegexField(
		max_length = 80,
		regex = '^(.*[^0-9]+) (([1-9][0-9]*)/)?([1-9][0-9]*[a-cA-C]?)$'
	)
	customer_city = forms.CharField(max_length=80)
	customer_psc = forms.RegexField(regex='\d{3} ?\d{2}')


class Order(models.Model):
	wallet_address = models.OneToOneField(
		max_length = 34,
		primary_key = True
	)
	product = models.CharField(max_length=30)
	count = models.IntegerField()
	customer = models.CharField(max_length=60)
	email = models.CharField(max_length=80)
	customer_address = models.CharField(max_length=80)
	customer_city = models.CharField(max_length=80)
	customer_psc = models.CharField(max_length=10)
	created = models.DateTimeField(auto_now_add=True)
	transaction_accepted = models.BooleanField(default=False)

	class Meta:
		ordering = ['-created']

	def __unicode__(self):
		return u'%s' % self.wallet_address

class Addresses(models.Model):
	id = models.AutoField(primary_key=True)
	wallet_address = models.CharField(max_length=34)

	def __unicode__(self):
		return u'%s' % self.wallet_address
