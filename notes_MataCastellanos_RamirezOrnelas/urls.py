from django.urls import path
from . import views

app_name = "notes_MataCastellanos_RamirezOrnelas"
urlpatterns = [
    path("",views.Lista_notas, name="Lista"),
    path("<int:id>/",views.Detalle_notas, name="Detalle"),
    path("new/", views.Creacion_notas, name="Creacion"),
    path("<int:id>/edit", views.Edicion_notas, name="Edicion"),
    path("<int:id>/delete/", views.Eliminacion_notas, name="Eliminacion")
]
