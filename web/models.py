from django.db import models
from django import forms

class MasterPublicKeys(models.Model):
	id = models.AutoField(primary_key=True)
	master_public_key = models.CharField(max_length=200,unique=True)

	def __unicode__(self):
		return u'%s' % self.master_public_key

class Products(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=30,unique=True)
	base_price = models.DecimalField(max_digits=16,decimal_places=8)
	master_public_key = models.ForeignKey(MasterPublicKeys)
	
	def __unicode__(self):
		return u'%s' % self.title
		
class Orders(models.Model):
	wallet_address = models.CharField(max_length=34,unique=True)
	price = models.DecimalField(max_digits=16,decimal_places=8)
	product = models.ForeignKey(Products)
	count = models.IntegerField()
	email = models.CharField(max_length=80)
	name = models.CharField(max_length=60)
	address = models.CharField(max_length=80)
	city = models.CharField(max_length=80)
	postcode = models.CharField(max_length=10)
	created = models.DateTimeField(auto_now_add=True)
	transaction_accepted = models.BooleanField(default=False)

	class Meta:
		ordering = ['-created']

	def __unicode__(self):
		return u'%s' % self.wallet_address

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
	email = forms.EmailField(max_length=80)
	name = forms.CharField(max_length=60)
	address = forms.RegexField(
		max_length = 80,
		regex = '^(.*[^0-9]+) (([1-9][0-9]*)/)?([1-9][0-9]*[a-cA-C]?)$'
	)
	city = forms.CharField(max_length=80)
	postcode = forms.RegexField(regex='\d{3} ?\d{2}')
