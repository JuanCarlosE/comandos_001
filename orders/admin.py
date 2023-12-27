from django.utils.html import format_html
from django.contrib import admin
from .models import Order,OrderDetail

# Conjunction between the models.

class InlineOrderDetail(admin.TabularInline):
    model = OrderDetail
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [InlineOrderDetail]
    list_display = ["id","soldier","facturarBtn"]
    change_form_template = 'admin/order_detail.html'

    def facturarBtn(self, obj):
        return format_html('<a class="btn", href="/soldiers/factura/'+str(obj.id)+'">Facturar</a>',obj.id)
    facturarBtn.short_description = 'Acción'

# Register your models here.
admin.site.register(Order,OrderAdmin)