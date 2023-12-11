from django.db import models
from products.models import ProductServ
from soldiers.models import Soldier

# Create your models here.

class Order(models.Model):
    soldier = models.ForeignKey(Soldier,on_delete=models.CASCADE,verbose_name= "Soldado:")
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate= models.DateTimeField(auto_now=True)
    methodPayment = models.CharField(max_length=50,verbose_name= "Método de pago:")
    orderProducts = models.ManyToManyField(ProductServ,through="OrderDetail")
    def __str__(self):
        return "Factura No. " + str(self.id) + " Usuario: " + self.soldier.names
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductServ,on_delete=models.CASCADE,verbose_name= "Producto:")
    quantity = models.IntegerField(default=1,verbose_name= "Cantidad:")
    startSuscription = models.DateField(blank=True,null=True,verbose_name= "Inicio de suscripción:")
    endSuscription= models.DateField(blank=True,null=True,verbose_name= "Fin de suscripción:")
    def __str__(self):
        return "orderDetailId: "+ str(self.id)
    def getId(self):
        return self.id

    def getProduct (self):
        return self.product

    def getEndSuscription (self):
        return self.endSuscription
    
    class Meta:
        verbose_name = "Detalles de la Factura"
        verbose_name_plural = "Detalles de las Facturas"

