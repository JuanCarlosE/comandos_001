from django.db import models

# Create your models here.

class Soldier(models.Model):
    names = models.CharField(max_length=100,verbose_name= "Nombres:")
    lastNames = models.CharField(max_length=100,verbose_name= "Apellidos:")
    rh = models.CharField(max_length=3, blank=True,verbose_name= "RH:")
    age = models.SmallIntegerField(verbose_name= "Edad:")
    phoneNumber = models.CharField(max_length=20,unique=True,verbose_name= "No. celular:")
    userPhoto = models.ImageField(upload_to ='photos/',max_length=100,verbose_name= "Foto:", blank=True)
    notes = models.TextField(blank=True,verbose_name= "Observaciones:")
    def __str__(self):
        return self.names + " " + self.lastNames

    def getId (self): 
        return self.id
    class Meta:
        verbose_name = "Soldado"
        verbose_name_plural  =  "Soldados"

class Measures(models.Model):
    soldier = models.ForeignKey(Soldier,on_delete=models.CASCADE)
    weight = models.FloatField(null=True,blank=True,verbose_name= "Peso:")
    height = models.FloatField(null=True,blank=True,verbose_name= "Altura:")
    shoulders = models.FloatField(null=True,blank=True,verbose_name= "Hombros:")
    abds = models.FloatField(null=True,blank=True,verbose_name= "Abdomen:")
    pectoral = models.FloatField(null=True,blank=True,verbose_name= "Pectorales:")
    leftBicep = models.FloatField(null=True,blank=True,verbose_name= "Bicep izquierdo:")
    rightBicep = models.FloatField(null=True,blank=True,verbose_name= "Bicep derecho:")
    leftForearm = models.FloatField(null=True,blank=True,verbose_name= "Antebrazo izquierdo:")
    rightForearm = models.FloatField(null=True,blank=True,verbose_name= "Antebrazo derecho:")
    leftLeg = models.FloatField(null=True,blank=True,verbose_name= "Pierna izquierda:")
    RightLeg = models.FloatField(null=True,blank=True,verbose_name= "Pierna derecha:")
    neck = models.FloatField(null=True,blank=True,verbose_name= "Cuello:")
    ass = models.FloatField(null=True,blank=True,verbose_name= "Gluteo:")

    class Meta:
        verbose_name = "Medida"
        verbose_name_plural  =  "Medidas"

from orders.models import Order
class Assistence(models.Model):
    soldier = models.ForeignKey(Soldier,on_delete=models.CASCADE,verbose_name= "Soldado:")
    registerDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(verbose_name = "Estado")
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True,verbose_name= "Factura:")
    def __str__(self):
        return "Asistencia No: " + str(self.id) + " || " + self.soldier.names

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural  =  "Asistencias"

