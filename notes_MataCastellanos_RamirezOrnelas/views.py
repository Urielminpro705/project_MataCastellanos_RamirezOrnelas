from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Note
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.
def Lista_notas(request):
    lista_notas = Note.objects.select_related("user").all().order_by("user__id")
    context = {"Lista_notas":lista_notas}
    return render(request, "notes_MataCastellanos_RamirezOrnelas/note_list_MataCastellanos_RamirezOrnelas.html", context)

def Detalle_notas(request, id):
    nota = get_object_or_404(Note, pk=id)
    context = {"Nota":nota}
    return render(request, "notes_MataCastellanos_RamirezOrnelas/note_detail_MataCastellanos_RamirezOrnelas.html", context)

def Creacion_notas(request):
    usuarios = User.objects.all()
    context = {"Lista_usuarios":usuarios, "url":request.get_full_path()}

    if request.method == 'POST':
        id_usuario = request.POST.get("usuarios")
        titulo = request.POST.get("titulo")
        contenido = request.POST.get("contenido")

        if id_usuario and titulo and contenido:
            usuario = get_object_or_404(User, pk=id_usuario)  # Obtener el usuario por ID
            nota = Note.objects.create(user=usuario, title=titulo, content=contenido)
            return redirect(reverse('notes_MataCastellanos_RamirezOrnelas:Detalle',args=(nota.id,)))

    return render(request, "notes_MataCastellanos_RamirezOrnelas/note_edit_MataCastellanos_RamirezOrnelas.html", context)

def Edicion_notas(request, id):
    usuarios = User.objects.all()
    nota = get_object_or_404(Note, pk=id)
    context = {"Lista_usuarios":usuarios, "Nota":nota, "url":request.get_full_path()}

    if request.method == 'POST':
        id_usuario = request.POST.get("usuarios")
        titulo = request.POST.get("titulo")
        contenido = request.POST.get("contenido")

        if id_usuario and titulo and contenido:
            usuario = get_object_or_404(User, pk=id_usuario)  # Obtener el usuario por ID
            nota = get_object_or_404(Note, pk=id)
            nota.title = titulo
            nota.content = contenido
            nota.user = usuario
            nota.save()
            return redirect(reverse('notes_MataCastellanos_RamirezOrnelas:Detalle',args=(nota.id,)))
    return render(request, "notes_MataCastellanos_RamirezOrnelas/note_edit_MataCastellanos_RamirezOrnelas.html/", context)

def Eliminacion_notas(request, id):
    nota = get_object_or_404(Note, pk=id)
    nota.delete()
    return redirect("notes_MataCastellanos_RamirezOrnelas:Lista")