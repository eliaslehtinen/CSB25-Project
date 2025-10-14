from django.shortcuts import render
from django.http import HttpResponse
from .models import Note

def mainPageView(request):
    user = request.user
    notes = Note.objects.filter(owner=user).values()
    context = {"user": user, "notes": notes}
    return render(request, "notes/index.html", context)

def noteView(request, note_id):
    return HttpResponse("Not implemented")

def createNote(request):
    return HttpResponse("Not implemented")

def deleteNote(request, note_id):
    return HttpResponse("Not implemented")