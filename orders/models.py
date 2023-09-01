from django.db import models
from products.models import ProductServ
from soldiers.models import Soldier

# Create your models here.

class Order(models.Model):
    soldier = models.ForeignKey(Soldier,on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate= models.DateTimeField(auto_now=True)
    methodPayment = models.CharField(max_length=50)
    orderProducts = models.ManyToManyField(ProductServ,through="OrderDetail")
    def __str__(self):
        return "Orden No: " + str(self.id) + " Usuario: " + self.soldier.names

class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductServ,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    startSuscription = models.DateTimeField(blank=True,null=True)
    endSuscription= models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return "orderDetailId: "+ str(self.id)
    def getId(self):
        return self.id

    def getProduct (self):
        return self.product

    def getEndSuscription (self):
        return self.endSuscription
