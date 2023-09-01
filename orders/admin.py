from django.contrib import admin
from .models import Order,OrderDetail

# Conjunction between the models.

class InlineOrderDetail(admin.TabularInline):
    model = OrderDetail
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [InlineOrderDetail]

# Register your models here.
admin.site.register(Order,OrderAdmin)