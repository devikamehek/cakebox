from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cake(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=250)
    flavour=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    shape=models.CharField(max_length=200)
    weight=models.PositiveIntegerField()
    layer=models.PositiveIntegerField()
    cake_pic=models.ImageField(upload_to="images",null=True,blank=True)
    description=models.CharField(max_length=250)
    

    def __str__(self) -> str:
        return self.name
