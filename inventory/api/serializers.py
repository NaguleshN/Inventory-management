from django.contrib.auth.models import Group,User
from rest_framework import serializers
from invention.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['name','permissions']
        
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model=Product
        fields="__all__"


class LogSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model=Log
        fields=['product','quantity','created_at','status','acting','due_date']