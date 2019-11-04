from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name=models.CharField(max_length=20)
    category=models.CharField(max_length=10)
    text=models.TextField()
    price=models.FloatField(default=0)
    image=models.ImageField(upload_to='image', blank=True,null=True)
    saler=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name

class korzina(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,blank=True,null=True)