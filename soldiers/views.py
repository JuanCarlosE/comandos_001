import datetime
from django.utils import timezone
from products.models import ProductServ
from django.shortcuts import render
from django.http import HttpResponse
from .models import Soldier,Assistence
from django.http import JsonResponse
from orders.models import Order,OrderDetail
from templates.factura.invoice import makePdf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.
#Lleva a index page.
def home(request):
    return render (request, "home.html")

#Lleva a la pagina que habilita el registro de usuarios a partir de su numero celular.
def phoneRegister(request):
    return render (request, "phoneRegis.html")

def asisRegister(request):
    usr = ''
    now = timezone.localtime(timezone.now())
    phone = request.POST.get("phone")
    suscriActivas = "null"
    asistencia = "null"

    try:
        usr = Soldier.objects.get(phoneNumber=phone)
    except ObjectDoesNotExist:
        return render(request, 'alerts.html', {"message":1})#"El usuario aun no esta registrado."

    ordenSuscri = Order.objects.filter(soldier = usr.getId())

    if (ordenSuscri.count() > 0 ):
        for pedido in ordenSuscri:
            ordenEnProduct = OrderDetail.objects.filter(order = pedido)

            for itemOrder in ordenEnProduct:
                if(itemOrder.product.category == "suscripcion" and itemOrder.endSuscription >= now):
                    suscriActivas = pedido

        asisExist = Assistence.objects.filter(registerDate__year=now.year, registerDate__month=now.month,registerDate__day=now.day,soldier_id=usr)
        if asisExist.count() == 0:
            if suscriActivas == "null":
                asistencia = Assistence(soldier=usr,status=False)#Tengo que revisar esto.
                #asistencia.save()
            else:
                asistencia = Assistence(soldier=usr, status=True, orderId=suscriActivas)
                asistencia.save()
            return render (request, 'alerts.html', {"message":2})#"Registro satisfactorio."
        else:
            return render (request, 'alerts.html', {"message":3} )#"El usuario ya asistió el dia de hoy."
    else: 
        asistencia = Assistence(soldier=usr,status=False)
        asistencia.save()
        return render (request, 'alerts.html', {"message":4})#"El usuario no tiene ninguna orden de suscripcion registrada."

def viewCalendar(request):
    return render(request, "reports.html")

'''
def viewAsistenciabyDay(request, year, month, day):
    asistenciByDay = Assistence.objects.filter(registerDate__year=year, registerDate__month=month,registerDate__day=day)
    countByDay = asistenciByDay.count()
    assis2 = Assistence.objects.all()
    context = {
        "listaAsistencia": asistenciByDay,
    }
    return render (request, 'assistencebyday.html' ,context)
'''
def countCalendar(request, year,month,day,year2,month2,day2):
    #Dias
    fecha1 = datetime.date(year,month,day)
    fecha2 = datetime.date(year2,month2,day2)

    if fecha2 != fecha1:
        #Asistencia general
        rangeGeneral = Assistence.objects.filter(registerDate__range=(fecha1, fecha2)).count()
        #Asistencia tramposos
        rangeTramposos = Assistence.objects.filter(registerDate__range=(fecha1, fecha2),status=False).count()
        return JsonResponse ({"totalAsistencia": rangeGeneral, "totalTramposos": rangeTramposos}, safe=False)
    else:
        #Dia 2 agregandole un dia extra.
        fecha2 = datetime.date(year2, month2, day2) + datetime.timedelta(days=1)

        #Asistencia general
        rangeGeneral = Assistence.objects.filter(registerDate__range=(fecha1, fecha2)).count()
        #Asistencia tramposos
        rangeTramposos = Assistence.objects.filter(registerDate__range=(fecha1, fecha2),status=False).count()
        return JsonResponse ({"totalAsistencia": rangeGeneral, "totalTramposos": rangeTramposos}, safe=False)


def viewTramposos(request, year,month,day,year2,month2,day2):
    #Dias
    date1 = str(year)+'-'+str(month)+'-'+str(day)+' 00:00:00'
    date2 = str(year2)+'-'+str(month2)+'-'+str(day2)+' 23:59:59'
    fecha1 = datetime.date(year,month,day)
    fecha2 = datetime.date(year2,month2,day2)

    tramp = Assistence.objects.filter(registerDate__range=(date1,date2),status=False).order_by('registerDate')
    context = {
        "fecha1": fecha1,
        "fecha2": fecha2,
        "trampososList": tramp
    }
    return render(request, 'tramposos.html',context)

def viewRange(request,year,month,day,year2,month2,day2):
    #Dias
    fecha1 = datetime.date(year,month,day)
    fecha2 = datetime.date(year2,month2,day2)
    date1 = str(year)+'-'+str(month)+'-'+str(day)+' 00:00:00'
    date2 = str(year2)+'-'+str(month2)+'-'+str(day2)+' 23:59:59'

    #if date2 != date1:
    range = Assistence.objects.filter(registerDate__range=(date1,date2)).order_by('registerDate')
    context = {
        "fecha1": fecha1,
        "fecha2": fecha2,
        "rangeList": range
    }
    return render(request, 'rango.html',context)

def viewMorosos(request):
    morosos = []
    paso1 = OrderDetail.objects.filter(product=2)
    for o in paso1:
        paso2 = (o.order.id)
        paso3 = Assistence.objects.filter(order=paso2).count()
        if paso3 > 12:
            dictmorosos = {"nombre": o.order.soldier.names, 'factura': o.order.id, 'fechaVencimiento': o.endSuscription,  "diasextra":paso3-12}
            morosos.append(dictmorosos)
    context = {
        "morososList": morosos
    }
    return render (request,"morosos.html", context)

def viewInvoice(request,id):
    data = Order.objects.filter(id=id).get()
    nameItem = OrderDetail.objects.filter(order=id).get()
    valueItem = ProductServ.objects.filter(name=nameItem.product).get()
    items = [
        {
            'producto':nameItem.product,
            'cantidad':nameItem.quantity,
            'valorProd':valueItem.price,
            
        }
    ]
    total = sum([i['valorProd'] for i in items])
    info = {"numFactura":data.id, "fechaCreacion":data.creationDate.date, "client":data.soldier, 
            "pagoMeto":data.methodPayment, "items":items,"final":nameItem.endSuscription.date,"totalFactu":total}
    return render (request, "invTemplate.html",info)