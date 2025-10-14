from django.urls import path

from .views import mainPageView, createNote, deleteNote, noteView

urlpatterns = [
    path("", mainPageView, name="main"),
    path("create/", createNote, name="create"),
    path("<int:note_id>/view/", noteView, name="view note"),
    path("<int:note_id>/delete/", deleteNote, name="delete"),
]