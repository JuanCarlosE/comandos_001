from django.urls import path
from . import views

app_name= "soldiers"
urlpatterns = [
    path('', views.home, name='home'),
    path("check/", views.phoneRegister, name='check'), #Obtiene y envia el numero de celular para filtrar a partir de el.
    path("save/", views.asisRegister), #Guarda el intento de asistencia del usuario con o sin orden activa. 
    path("calendar/", views.viewCalendar, name='calendar'), #Envia un calendario apartir del cual se podra observar los registros por dia.
    #path("assistence/<str:year>/<str:month>/<str:day>", views.viewAsistenciabyDay), #Envia la lista de los registros segun el dia seleccionado en el calendario.
    path("api/calendar/<int:year>/<int:month>/<int:day>/to/<int:year2>/<int:month2>/<int:day2>", views.countCalendar), #Envia un conteo con el numero total de asistencias por categoria.
    path("cheaters/<int:year>/<int:month>/<int:day>/to/<int:year2>/<int:month2>/<int:day2>", views.viewTramposos), #Envia una lista con los usuarios "tramposos" por el rango de fecha puesto (que asisten luego de que su mensualidad haya vencido.)
    path("range/<int:year>/<int:month>/<int:day>/to/<int:year2>/<int:month2>/<int:day2>", views.viewRange), #Envia una lista con los registros hechos dentro de un periodo de tiempo.
    path("morosos/", views.viewMorosos, name='morosos'), #Envia una lista con los usuarios "morosos" (que van mas de los 15 dias pagos.)
    path("factura/<str:id>", views.viewInvoice)
]