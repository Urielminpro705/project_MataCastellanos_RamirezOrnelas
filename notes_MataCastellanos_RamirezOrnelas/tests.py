from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note

class Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            first_name="Test",
            last_name="User"
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='12345',
            first_name="Test2",
            last_name="User2"
        )
        self.nota = Note.objects.create(title="Nota de prueba",content="Contenido de la nota de prueba", user=self.user)
        self.nota = Note.objects.create(title="Nota de prueba2",content="Contenido de la nota de prueba2", user=self.user2)

    def test_carga_lista(self):
        response = self.client.get(reverse("notes_MataCastellanos_RamirezOrnelas:Lista"))

        # Comprobar que la solicitud fue correcta
        self.assertEqual(response.status_code, 200)

        # Comprueba que se use el template de lista
        self.assertTemplateUsed(response, "notes_MataCastellanos_RamirezOrnelas/note_list_MataCastellanos_RamirezOrnelas.html")

        # Comprobar que las notas si esten en la respuesta
        self.assertContains(response, "Nota de prueba")
        self.assertContains(response, "Nota de prueba2")

    def test_creacion(self):
        # Prueba del formulario
        response = self.client.post(reverse("notes_MataCastellanos_RamirezOrnelas:Creacion"),{
            "usuarios": self.user.id,
            "titulo": "Nota test",
            "contenido": "Nota de prueba muy epica"
        })

        # Comprobar redireccion
        self.assertEqual(response.status_code, 302)

        # Comprobar que si se creó
        self.assertTrue(Note.objects.filter(title='Nota test').exists())

    def test_creacion_vacio(self):
        # Prueba del formulario
        response = self.client.post(reverse("notes_MataCastellanos_RamirezOrnelas:Creacion"),{
            "usuarios": self.user.id,
            "titulo": "Nota test",
            "contenido": ""
        })

        # Comprobar que no hubo redireccionamiento
        self.assertEqual(response.status_code, 200)

        # Comprobar que no se creó
        self.assertFalse(Note.objects.filter(title='Nota test').exists())

    def test_actualizacion(self):
        # Prueba del formulario
        response = self.client.post(reverse("notes_MataCastellanos_RamirezOrnelas:Edicion", args=[self.nota.id]),{
            "usuarios": self.user2.id,
            "titulo": "Nota actualiza",
            "contenido": "Nota de prueba muy epica actualizada"
        })

        # Comprobar redireccion
        self.assertEqual(response.status_code, 302)

        # Verificar que se aplicaron los cambios
        self.nota.refresh_from_db()
        self.assertEqual(self.nota.user, self.user2)
        self.assertEqual(self.nota.title, "Nota actualiza")
        self.assertEqual(self.nota.content, "Nota de prueba muy epica actualizada")

    def test_actualizacion_vacio(self):
        # Prueba del formulario
        response = self.client.post(reverse("notes_MataCastellanos_RamirezOrnelas:Edicion", args=[self.nota.id]),{
            "usuarios": self.user2.id,
            "titulo": "",
            "contenido": "Nota de prueba muy epica actualizada"
        })

        # Comprobar que no hubo redireccion
        self.assertEqual(response.status_code, 200)

        # Verificar que no se aplicaron los cambios
        self.nota.refresh_from_db()
        self.assertEqual(self.nota.user, self.user2)
        self.assertNotEqual(self.nota.title, "")
        self.assertNotEqual(self.nota.content, "Nota de prueba muy epica actualizada")

    def test_eliminacion(self):
        response = self.client.post(reverse("notes_MataCastellanos_RamirezOrnelas:Eliminacion", args=[self.nota.id]))

        # Comprobar redireccion
        self.assertEqual(response.status_code, 302)

        # Comprobar que si se eliminó
        self.assertFalse(Note.objects.filter(id=self.nota.id).exists())