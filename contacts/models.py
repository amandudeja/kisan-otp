from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Contact(models.Model):
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	mobile = models.BigIntegerField()



	def __str__(self):
		return self.first_name + self.last_name


	def get_absolute_url(self):

		return reverse('contacts:detail',
						args=[self.id,])

class Sent(models.Model):
	mobile = models.ForeignKey(Contact,related_name='messages',on_delete=models.CASCADE)
	sent_time = models.DateTimeField(null=True)
	otp = models.CharField(max_length=10,default=000000)


	def __str__(self):

		return "Sent to: "+self.mobile.first_name+" at "+str(self.sent_time)
