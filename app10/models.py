from django.db import models 
from django.contrib.auth.models import User


# Create your models here.
class AddCategoryModel(models.Model):
	name=models.CharField(max_length=30)
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class AddSubscriptionModel(models.Model):

	name=models.CharField(max_length=30)
	duration=models.CharField(max_length=30)
	feestructure=models.IntegerField()
	category=models.CharField(max_length=30,default='')
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)
	


	def __str__(self):
		return self.name

class SubBookModel(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	name=models.CharField(max_length=30)
	duration=models.CharField(max_length=30)
	feestructure=models.IntegerField()
	category=models.CharField(max_length=30,default='')
	status=models.BooleanField(default=True)
	payment_status=models.BooleanField(default=False)
	created_on=models.DateTimeField(auto_now=True)



