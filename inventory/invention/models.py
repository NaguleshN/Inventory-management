from django.db import models

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=10)
    decription=models.CharField(max_length=100)
    actual_count=models.PositiveIntegerField()
    available_count=models.PositiveIntegerField()
    # category=
 
class Category(models.Model):
    name=models.CharField(max_length=25)
    # created_by =
    created_at=models.DateTimeField()
    
class Logs(models.Model):
    roll_number=models.CharField(max_length=8)
    name=models.CharField(max_length=25)
    time_logged=models.DateTimeField()
    # status=model
    no_of_checks=models.PositiveIntegerField()
    
    
class Cart(models.Model):
    Roll_number=models.CharField(max_length=8)
    # product_name=models.ForeignKey("Product.Model", on_delete=models.CASCADE)(max_length=20)
    quantity=models.PositiveIntegerField()
    due_date=models.DateTimeField()


class Wastage(models.Model):
    roll_number=models.CharField(max_length=8)
    # product_name=models.ForeignKey("Product.Model", on_delete=models.CASCADE)(max_length=20)
    quantity=models.PositiveIntegerField()
    reason=models.TextField()