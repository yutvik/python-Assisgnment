from django.db import models
from app_buyer.models import *
# Create your models here.
class seller_User(models.Model):
    picture=models.FileField(upload_to="media/",default="msm.jpg")
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    
    
class Product(models.Model):
    p_name=models.CharField(max_length=50)
    p_price=models.IntegerField()
    p_image=models.FileField(upload_to="Product/",default="msm.jpg")
    p_qut=models.IntegerField()
    p_dec=models.TextField(max_length=500)
    seller_id=models.ForeignKey(seller_User, on_delete=models.CASCADE)
    
    

    

   
 
