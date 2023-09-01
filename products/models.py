from django.db import models

# Create your models here.

class ProductServ(models.Model):

    PRODUCT = "PROD"
    SERVICE = "SERV"
    SUBSCRIPTION = "SUBS"
    
    categoryChoices=[
        (PRODUCT, "Producto"),
        (SERVICE, "Servicio"),
        (SUBSCRIPTION, "Suscripcion ")
    ]

    name = models.CharField(max_length=150)
    descrip = models.TextField(blank=True,null=True)
    category = models.CharField(max_length=4, choices=categoryChoices,default=SUBSCRIPTION)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate= models.DateTimeField(auto_now=True)
    status = models.BooleanField(verbose_name = "Activo") 
    price = models.IntegerField()
    def __str__(self):
        return self.name