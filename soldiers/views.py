import datetime
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from .models import Soldier,Assistence
from orders.models import Order,OrderDetail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.
#Lleva a index page.
def  index(request):
    return render (request, "index.html")
#Lleva a la pagina que habilita el registro de usuarios a partir de su numero celular.
def phoneRegister(request):
    return render (request, "phoneRegis.html")

def asisRegister(request):
    usr = ''
    now = timezone.now()
    phone = request.POST.get("phone")
    suscriActivas = "null"
    asistencia = "null"

    try:
        usr = Soldier.objects.get(phoneNumber=phone)
    except ObjectDoesNotExist:
        return HttpResponse("El usuario aun no esta registrado.")

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
                asistencia = Assistence(soldier=usr,status=False)
            else:
                asistencia = Assistence(soldier=usr, status=True, orderId=suscriActivas)
            asistencia.save()
            return HttpResponse ("Registro satisfactorio.")
        else:
            return HttpResponse ("El usuario ya asistió el dia de hoy.")
    else: 
        asistencia = Assistence(soldier=usr,status=False)
        asistencia.save()
        return HttpResponse ("El usuario no tiene ninguna orden de suscripcion registrada.")

def viewCalendar(request):
    return render(request, "reports.html")

def viewAsistenciabyDay(request, year, month, day):
    asistenciByDay = Assistence.objects.filter(registerDate__year=year, registerDate__month=month,registerDate__day=day)
    context = {
        "listaAsistencia": asistenciByDay
    }
    return render (request, "assistencebyday.html", context)

def viewTramposos(request, year, month, day):
    tramp = Assistence.objects.filter(registerDate__year=year,registerDate__month=month,registerDate__day=day,status=False)
    context = {
        "trampososList": tramp,
    }
    return render(request, 'tramposos.html',context)

def viewRange(request,year,month,day,year2,month2,day2):
    date1 = datetime.date(year,month,day)
    date2 = datetime.date(year2,month2,day2)
    range = Assistence.objects.filter(registerDate__range=(date1, date2))
    context = {
        "fecha1": date1,
        "fecha2": date2,
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
            dictmorosos = {"nombre": o.order.soldier.names, "diasextra":paso3-12}
            morosos.append(dictmorosos)
    context = {
        "morososList": morosos
    }
    return render (request,"morosos.html", context)