from django.contrib import admin
from .models import Soldier,Measures,Assistence

# Conjunction between the models.

class inlineMeasures(admin.TabularInline):
    model = Measures
    extra = 1

class MeasuresAdmin(admin.ModelAdmin):
    inlines = [inlineMeasures]

# Register your models here.
admin.site.register(Soldier,MeasuresAdmin)
admin.site.register(Assistence)