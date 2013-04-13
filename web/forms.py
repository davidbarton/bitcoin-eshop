# -*- coding: utf-8 -*-
from django import forms

class ProductForm(forms.Form):
	product = forms.CharField(
		widget = forms.HiddenInput(),
		initial = ''
	)
	count = forms.IntegerField(
		max_value = 20,
		min_value = 1,
		initial = 1
	)
	def set_product(self, product, max_value = 20):
		self.fields['product'].initial = product
		self.fields['count'] = forms.IntegerField(
			max_value = max_value,
			min_value = 1,
			initial = 1
		)

class ContactInformationForm(forms.Form):
	product = forms.CharField(widget=forms.HiddenInput())
	count = forms.IntegerField(widget=forms.HiddenInput())
	email = forms.EmailField(max_length=80)
	name = forms.CharField(max_length=60, label='Celé jméno')
	address = forms.RegexField(
		max_length = 80,
		regex = '^(.*[^0-9]+) (([1-9][0-9]*)/)?([1-9][0-9]*[a-cA-C]?)$',
		label = 'Ulice a č.p.'
	)
	city = forms.CharField(max_length=80, label='Město')
	postcode = forms.RegexField(regex='\d{3} ?\d{2}', label='PSČ')