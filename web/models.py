from django.db import models

class Order(models.Model):
	wallet_address = models.CharField(max_length=34)
	product = models.CharField(max_length=30)
	count = models.IntegerField()
	customer = models.CharField(max_length=60)
    email = models.CharField(max_length=80)
    customer_address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    transaction_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s' % self.wallet_address