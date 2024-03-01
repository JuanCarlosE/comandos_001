import os
import base64
import datetime
from weasyprint import HTML
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from .models import Soldier,Assistence
from products.models import ProductServ
from orders.models import Order,OrderDetail
from django.templatetags.static import static
from django.http import JsonResponse,HttpResponse,FileResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.
#Lleva a las paginas que los clientes visualizarán.
def home(request):
    return render (request, "clientsPages/home.html")
def services(request):
    return render (request, "clientsPages/services.html")
def plants(request):
    return render (request, "clientsPages/plants.html")

@login_required
#Lleva a la pagina que habilita el registro de usuarios a partir de su numero celular.
def phoneRegister(request):
    return render (request, "phoneRegis.html")

@login_required
def asisRegister(request):
    now = timezone.localtime(timezone.now())
    phone = request.POST.get("phone")
    
    
    try:
        usr = Soldier.objects.get(phoneNumber=phone)#Obtiene el usuario al que le pertenece el No celular.
    except Soldier.DoesNotExist:
        return JsonResponse ({"message": 1, "info":None}, safe=False)#"El usuario aun no esta registrado."
    
    try:
        userInFactura = Order.objects.filter(soldier=usr).all() #Obtiene las ordenes que tiene el usuario vinculadas.
        suscriActivas = OrderDetail.objects.filter(order__in=userInFactura,endSuscription__gte=now).get()
    except ObjectDoesNotExist:
        suscriActivas = None

    asisExist = Assistence.objects.filter(
        registerDate__year=now.year,
        registerDate__month=now.month,
        registerDate__day=now.day,
        soldier=usr
    )
    try:
        dataUsr={"photo_url":usr.userPhoto.url,"nombreSold":usr.names,"apellidoSold":usr.lastNames,
             "dateEnd":suscriActivas.endSuscription}
    except:
        dataUsr={"photo_url":usr.userPhoto.url,"nombreSold":usr.names,"apellidoSold":usr.lastNames,
             "dateEnd":"No tiene una suscripción activa"}

    if asisExist.exists():
        return JsonResponse ({"message": 3, "info":dataUsr}, safe=False)#El usuario ya asistió el dia de hoy.
    elif suscriActivas:
        Assistence.objects.create(soldier=usr, status=True, order=suscriActivas.order, registerDate=now)
        return JsonResponse ({"message": 2, "info":dataUsr}, safe=False)#Registro satisfactorio.
    else: 
        Assistence.objects.create(soldier=usr, status=False, order=None, registerDate=now)
        return JsonResponse ({"message": 4, "info": dataUsr}, safe=False)#El usuario no tiene ninguna orden de suscripcion registrada.

@login_required
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

@login_required
def countCalendar(request, year,month,day,year2,month2,day2):
    #Dias
    fecha1 = str(year)+'-'+str(month)+'-'+str(day)+' 00:00:00'
    fecha2 = str(year2)+'-'+str(month2)+'-'+str(day2)+' 23:59:59'

    rangeGeneral = Assistence.objects.filter(registerDate__range=(fecha1, fecha2)).count()
    rangeTramposos = Assistence.objects.filter(registerDate__range=(fecha1, fecha2),status=False).count()
    return JsonResponse ({"totalAsistencia": rangeGeneral, "totalTramposos": rangeTramposos}, safe=False)

@login_required
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

@login_required
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

@login_required
def viewMorosos(request):
    morosos = []
    paso1 = OrderDetail.objects.filter(product=2)
    for o in paso1:
        paso2 = (o.order.id)
        paso3 = Assistence.objects.filter(order=paso2).count()
        if paso3 > 12:
            dictmorosos = {"nombre": o.order.soldier.names, 'factura': o.order.id, 'fechaVencimiento': o.endSuscription,  "diasextra":paso3-12,"perfil":o.order.soldier.id}
            morosos.append(dictmorosos)
    context = {
        "morososList": morosos
    }
    return render (request,"morosos.html", context)

@login_required
def viewInvoice(request,id):
    # Invoice data
    logo_url = request.build_absolute_uri(static('images/logo.png'))
    data = Order.objects.filter(id=id).latest('id')
    nameItem = OrderDetail.objects.filter(order=id).get()#Pregunta si aca siempre buscaria la orden actual en la que esta.
    valueItem = ProductServ.objects.filter(name=nameItem.product).get()
    items = [
        {
            'producto':nameItem.product,
            'cantidad':nameItem.quantity,
            'valorProd':valueItem.price,   
        }
    ]
    total = sum([i['valorProd'] for i in items])

    try:

        email = EmailMultiAlternatives(
            subject = 'Bienvenido a la familia Comandos Gym',
            body = 'Hola ¿como estas? aqui esta tu factura',
            from_email = 'comandosgym@hotmail.com',
            to = [data.soldier.email],
        )

        info = {
            "numFactura":data.id,
            "fechaCreacion":data.creationDate.date,
            "client":data.soldier, 
            "pagoMeto":data.methodPayment,
            "items":items,
            "final":nameItem.endSuscription.date,
            "totalFactu":total,
            "logo":logo_url
        }

        # Create pdf file with template 'invTemplate.html' 
        html_string = render_to_string('invTemplate.html',info)
        pdf_file = HTML(string=html_string).write_pdf()

        # Create path folders if doesn't exist
        download_folder = os.path.join(settings.BASE_DIR, 'Media', 'Invoices')
        os.makedirs(download_folder, exist_ok=True)
        file_path = os.path.join(download_folder, f'Factura-{id}.pdf')

        # Put the pdf file on path Media/Invoices  
        with open(file_path, 'wb') as f: # <-- 'WB' means write binary
            f.write(pdf_file)

        # Create pdf file view and download it
        response = FileResponse(open(file_path,"rb"))
        response['Content-Disposition'] = f'attachment; filename="Factura-{id}.pdf"'

        # Attach pdf file to email
        email.attach_file(file_path)

        # Send mail
        email.send()
        return response

    except:

        email = EmailMultiAlternatives(
            subject = 'Bienvenido a la familia Comandos Gym',
            body = 'Hola ¿como estas? aqui esta tu factura',
            from_email = 'comandosgym@hotmail.com',
            to = [data.soldier.email],
        )

        info = {
            "numFactura":data.id,
            "fechaCreacion":data.creationDate.date,
            "client":data.soldier, 
            "pagoMeto":data.methodPayment,
            "items":items,
            "final":"No aplica.",
            "totalFactu":total,
            "logo":logo_url
        }

        # Create pdf file with template 'invTemplate.html' 
        html_string = render_to_string('invTemplate.html',info)
        pdf_file = HTML(string=html_string).write_pdf()

        # Create path folders if doesn't exist
        download_folder = os.path.join(settings.BASE_DIR, 'Media', 'Invoices')
        os.makedirs(download_folder, exist_ok=True)
        file_path = os.path.join(download_folder, f'Factura-{id}.pdf')

        # Put the pdf file on path Media/Invoices  
        with open(file_path, 'wb') as f: # <-- 'WB' means write binary
            f.write(pdf_file)
        
        # Create pdf file view and download it
        response = FileResponse(open(file_path,"rb"))
        response['Content-Disposition'] = f'attachment; filename="Factura-{id}.pdf"'

        # Attach pdf file to email
        email.attach_file(file_path)
        
        # Send mail
        email.send()
        return response

@login_required
def viewProfile(request,id):
    data = Soldier.objects.filter(id=id).get()
    try:
        ord = Order.objects.filter(soldier_id=id).latest('id')
        invoice = OrderDetail.objects.filter(order_id=ord.id).get()
        info = {"photo_url":data.userPhoto.url,"nombreSold":data.names,"apellidoSold":data.lastNames,"dateEnd":invoice.endSuscription.date,
            "rh":data.rh,"phone":data.phoneNumber,"age":data.age,"notes":data.notes}
        return render (request, "profile.html",info)
    except ObjectDoesNotExist:
        info = {"photo_url":data.userPhoto.url,"nombreSold":data.names,"apellidoSold":data.lastNames,"dateEnd":"No tiene una suscripción activa",
            "rh":data.rh,"phone":data.phoneNumber,"age":data.age,"notes":data.notes}
        return render (request, "profile.html",info)     


