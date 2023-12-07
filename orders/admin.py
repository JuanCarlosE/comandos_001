from django.utils.html import format_html
from django.contrib import admin
from .models import Order,OrderDetail

# Conjunction between the models.

class InlineOrderDetail(admin.TabularInline):
    model = OrderDetail
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [InlineOrderDetail]
    list_display =["id","soldier","mi_boton_personalizado"]

    def mi_boton_personalizado(self, obj):
        return format_html('<a class="btn", href="/soldiers/factura/'+str(obj.id)+'">Facturar</a>',obj.id)
    mi_boton_personalizado.short_description = 'Acción'

# Register your models here.
admin.site.register(Order,OrderAdmin)