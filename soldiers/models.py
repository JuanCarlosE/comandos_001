from django.db import models

# Create your models here.

class Soldier(models.Model):
    names = models.CharField(max_length=100)
    lastNames = models.CharField(max_length=100)
    rh = models.CharField(max_length=3, blank=True)
    age = models.SmallIntegerField()
    phoneNumber = models.CharField(max_length=20,unique=True)
    notes = models.TextField(blank=True)
    def __str__(self):
        return self.names + " " + self.lastNames

    def getId (self): 
        return self.id
    class Meta:
        verbose_name = "Soldado"
        verbose_name_plural  =  "Soldados"

class Measures(models.Model):
    soldier = models.ForeignKey(Soldier,on_delete=models.CASCADE)
    weight = models.FloatField(null=True,blank=True)
    height = models.FloatField(null=True,blank=True)
    shoulders = models.FloatField(null=True,blank=True)
    abds = models.FloatField(null=True,blank=True)
    pectoral = models.FloatField(null=True,blank=True)
    leftBicep = models.FloatField(null=True,blank=True)
    rightBicep = models.FloatField(null=True,blank=True)
    leftForearm = models.FloatField(null=True,blank=True)
    rightForearm = models.FloatField(null=True,blank=True)
    leftLeg = models.FloatField(null=True,blank=True)
    RightLeg = models.FloatField(null=True,blank=True)
    neck = models.FloatField(null=True,blank=True)
    ass = models.FloatField(null=True,blank=True)

    class Meta:
        verbose_name = "Medida"
        verbose_name_plural  =  "Medidas"

from orders.models import Order
class Assistence(models.Model):
    soldier = models.ForeignKey(Soldier,on_delete=models.CASCADE)
    registerDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(verbose_name = "Activo:")
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return "Asistencia No: " + str(self.id) + " || " + self.soldier.names

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural  =  "Asistencias"

