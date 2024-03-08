from django.utils.html import format_html
from django.contrib import admin
from .models import Order,OrderDetail,ProductServ,Soldier
from import_export.formats import base_formats
from import_export import resources,fields
from import_export.widgets import ManyToManyWidget,ForeignKeyWidget,DateWidget
from import_export.fields import Field
from import_export.admin import ExportActionMixin

class exportOrder(resources.ModelResource):

    soldierName = fields.Field(
        column_name = 'Nombres',
        attribute = 'soldier',
        widget = ForeignKeyWidget(Soldier, field='names')
    )

    soldierLastName = fields.Field(
        column_name = 'Apellidos',
        attribute = 'soldier',
        widget = ForeignKeyWidget(Soldier, field='lastNames')
    )
    
    soldierPhone = fields.Field(
        column_name = 'No. Celular',
        attribute = 'soldier',
        widget = ForeignKeyWidget(Soldier, field='phoneNumber')
    )

    product = Field(
        column_name = 'Producto',
        attribute = 'orderProducts',
        widget = ManyToManyWidget(model=ProductServ,separator=',',field='name')
    )
    
    method = Field(
        column_name = 'Pagó con',
        attribute = 'methodPayment'
    )
    date = Field(
         column_name = 'Fecha creación',
         attribute = 'creationDate',
         widget = DateWidget('%d/%m/%Y')
    )

    class Meta:
        model = Order
        fields = ('soldierName','soldierLastName','soldierPhone','product','method','date') 

class InlineOrderDetail(admin.TabularInline):
    model = OrderDetail
    extra = 1

class OrderAdmin(ExportActionMixin,admin.ModelAdmin):
    inlines = [InlineOrderDetail]
    resource_class=exportOrder
    list_display = ["id","soldier","facturarBtn"]
    change_form_template = 'admin/order_detail.html'

    def facturarBtn(self, obj):
        return format_html('<a class="btn", href="/soldiers/factura/'+str(obj.id)+'">Facturar</a>',obj.id)
    facturarBtn.short_description = 'Acción'

    def get_export_formats(self):
            formats = (
                  #base_formats.CSV,
                  #base_formats.XLS,
                  base_formats.XLSX,
                  #base_formats.TSV,
                  #base_formats.ODS,
                  #base_formats.JSON,
                  #base_formats.YAML,
                  #base_formats.HTML,
            )
            return [f for f in formats if f().can_export()]

# Register your models here.
admin.site.register(Order,OrderAdmin)