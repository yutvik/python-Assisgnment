from django.db import models
from seller_buyer.models import *

# Create your models here.
class User(models.Model):
    picture=models.FileField(upload_to="media/",default="msm.jpg")
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.firstname)
    
    
class Cart(models.Model):
    pro_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    buyer_id=models.ForeignKey(User, on_delete=models.CASCADE)
    qut=models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    
    
    def __str__(self):
        return str(self.pro_id)
    
    
class Checkout(models.Model):
    FirstName=models.CharField(max_length=10)  
    MiddleName=models.CharField(max_length=10)
    LastName=models.CharField(max_length=10)
    Address=models.CharField(max_length=50)
    postelcode=models.IntegerField(default=0)
    State=models.CharField(max_length=10)
    PhoneNumber=models.IntegerField(default=0)
    


