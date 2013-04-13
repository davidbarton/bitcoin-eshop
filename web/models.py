from django.db import models

class MasterPublicKeys(models.Model):
	id = models.AutoField(primary_key=True)
	master_public_key = models.CharField(max_length=200,unique=True)

	def __unicode__(self):
		return u'%s' % self.master_public_key

class Products(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=30,unique=True)
	stock = models.IntegerField()
	img = models.CharField(max_length=100)
	base_price = models.DecimalField(max_digits=16,decimal_places=8)
	master_public_key = models.ForeignKey(MasterPublicKeys)

	class Meta:
		ordering = ['-title']
	
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
	transaction_status = models.IntegerField(default=0)

	class Meta:
		ordering = ['-created']

	def __unicode__(self):
		return u'%s' % self.wallet_address

class Variables(models.Model):
	title = models.CharField(max_length=30,unique=True)
	str_var = models.CharField(max_length=200,blank=True,null=True)
	int_var = models.IntegerField(blank=True,null=True)
	dec_var = models.DecimalField(max_digits=16,decimal_places=8,blank=True,null=True)

	def __unicode__(self):
		return u'%s' % self.title