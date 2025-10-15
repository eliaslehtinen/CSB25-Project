from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
import django.contrib.messages
from django import forms
from .models import Note
import datetime

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class CreateNoteForm(forms.Form):
    note_name = forms.CharField(max_length=30, required=True, label="Note name")
    note_content = forms.CharField(max_length=500, required=True, label="Content")

@login_required
def mainPageView(request):
    # Logged in user
    user = request.user
    # Text user uses to search for notes
    search = request.GET.get("search_text")
    if search == None:
        search = ""

    user_id = user.id
    query = "SELECT * FROM notes_note where owner_id={} AND note_name LIKE '%{}%'"
    notes = Note.objects.raw(query.format(user_id, search))

    # Fix for flaw 3:
    # Use safe built in methods like filter to create sql queries:
    #notes = Note.objects.filter(owner=user, note_name__icontains=search)

    context = {"user": user, "notes": notes, "search": search}
    return render(request, "notes/home.html", context)

def welcomeView(request):
    return render(request, "notes/index.html")

@login_required
def noteView(request, note_id):
    note = Note.objects.get(id=note_id)

    # Fix for flaw 1:
    # Check if the logged in user is the owner of the note
    #
    #if (note.owner != request.user):
    #    return HttpResponseRedirect("/notes/")

    return render(request, "notes/noteView.html", {"note": note})

@login_required
def createNote(request):
    if request.method == "POST":
        # Create note
        name = request.POST.get("note_name")
        content = request.POST.get("note_content")
        note = Note(
            note_name = name,
            note_content = content,
            created_date = datetime.datetime.now(),
            owner = request.user
        )
        note.save()
    return HttpResponseRedirect("/notes/")

@login_required
def deleteNote(request, note_id):
    if request.method == "POST":
        note = Note.objects.get(id=note_id)

        # Fix for flaw 1:
        # Check if the logged in user is the owner of the note
        #
        #if note.owner != request.user:
        #    return HttpResponseRedirect("/notes/")

        note.delete()
    return HttpResponseRedirect("/notes/")

def createAccount(request):
    form = CreateUserForm()
    if request.method == "POST":
        # Get form data and validate it
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            # Create new user: (email is None)
            user = User.objects.create_user(form.cleaned_data["username"], None, form_data["password"])
            user.save()
            # Authenticate and log the user in
            created_user = authenticate(username=form_data["username"], password=form_data["password"],)
            login(request, created_user)

            return HttpResponseRedirect("/notes/")
    return render(request, "notes/createUser.html", {"form": form})