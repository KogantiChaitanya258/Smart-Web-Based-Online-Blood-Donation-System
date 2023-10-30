from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class register(models.Model):
	Registeredname=models.CharField(max_length=40,primary_key=True)
	Email=models.CharField(max_length=40)
	Password=models.CharField(max_length=40)
	Mobile=models.IntegerField()

class donorregister(models.Model):
	username=models.CharField(max_length=40,primary_key=True)
	age=models.PositiveIntegerField()
	gender=models.CharField(max_length=40)
	city=models.CharField(max_length=40)
	address=models.CharField(max_length=60)
	contact=models.CharField(max_length=10)
	email=models.CharField(max_length=40)
	servicetype=models.CharField(max_length=10,default=None,null=True,blank=True)
	donortype=models.CharField(max_length=3)
	bloodgroup=models.CharField(max_length=3)
	date=models.DateField(max_length=40)
	ill=models.CharField(max_length=60)
	lastdonation_eligibility=models.CharField(max_length=15,default=None,null=True,blank=True)

class requests(models.Model):
	donorname=models.CharField(max_length=40)
	recievername=models.CharField(max_length=40)
	city=models.CharField(max_length=40)
	contact=models.CharField(max_length=10)
	requiredservice=models.CharField(max_length=10,default=None,null=True,blank=True)
	status=models.CharField(max_length=10,default='Pending',null=True,blank=True)

class bloodcamp(models.Model):
	campname=models.CharField(max_length=40,default=None)
	address=models.CharField(max_length=40,default=None)
	city=models.CharField(max_length=40,default=None)
	contact=models.CharField(max_length=10,default=None)
	organizername=models.CharField(max_length=10,default=None,null=True,blank=True)
	startdate=models.DateField(max_length=10,default=None,null=True,blank=True)
	enddate=models.DateField(max_length=10,default=None,null=True,blank=True)