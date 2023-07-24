from rest_framework import serializers
from app_buyer.models import *


class Checkout_serializers(serializers.ModelSerializer):
    	class Meta:
            model  =  Checkout
            fields  = '__all__'


