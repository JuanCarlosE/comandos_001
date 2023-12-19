from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.

class ProductServ(models.Model):

    PRODUCT = "PROD"
    SERVICE = "SERV"
    SUBSCRIPTION = "SUBS"
    
    categoryChoices=[
        (PRODUCT, "Producto"),
        (SERVICE, "Servicio"),
        (SUBSCRIPTION, "Suscripción")
    ]

    name = models.CharField(max_length=150,verbose_name= "Nombre:")
    descrip = models.TextField(blank=True,null=True,verbose_name= "Descripción:")
    category = models.CharField(max_length=4, choices=categoryChoices,default=SUBSCRIPTION,verbose_name= "Categoría:")
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate= models.DateTimeField(auto_now=True)
    status = models.BooleanField(verbose_name = "Estado") 
    price = MoneyField(max_digits=8,default_currency='COP',verbose_name= "Precio:")
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Producto/Servicio"
        verbose_name_plural  =  "Productos/Servicios"