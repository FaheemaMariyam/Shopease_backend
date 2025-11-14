from django.db import models

from cloudinary.models import CloudinaryField

class Category(models.Model):
    name=models.CharField(max_length=100)
    image=CloudinaryField('category_image',null=True,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    image=CloudinaryField('product_image',blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')

    def __str__(self):
        return self.name
