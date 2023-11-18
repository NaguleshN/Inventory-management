from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=10)
    decription=models.CharField(max_length=100)
    actual_count=models.PositiveIntegerField()
    available_count=models.PositiveIntegerField()
    # category=
 
class Category(models.Model):
    name=models.CharField(max_length=25)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Categories'
    
status=(('checked_in','checked_in'),('checked_out','checked_out'))
class Logs(models.Model):
    roll_number=models.CharField(max_length=8)
    name=models.CharField(max_length=25)
    time_logged=models.DateTimeField()
    status=models.TextChoices(choice=status)
    no_of_checks=models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Log'
    
    
class Cart(models.Model):
    Roll_number=models.CharField(max_length=8)
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    due_date=models.DateTimeField()


class Wastage(models.Model):
    roll_number=models.CharField(max_length=8)
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    reason=models.TextField()