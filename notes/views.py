from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
import django.contrib.messages
from django import forms
from .models import Note

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

@login_required
def mainPageView(request):
    user = request.user
    notes = Note.objects.filter(owner=user).values()
    context = {"user": user, "notes": notes}
    return render(request, "notes/home.html", context)

def welcomeView(request):
    return render(request, "notes/index.html")

@login_required
def noteView(request, note_id):
    return HttpResponse("Not implemented")

@login_required
def createNote(request):
    return HttpResponse("Not implemented")

@login_required
def deleteNote(request, note_id):
    return HttpResponse("Not implemented")

def createAccount(request):
    form = CreateUserForm()
    if request.method == "POST":
        # Get form data and validate it
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            # Create new user:
            user = User.objects.create_user(form.cleaned_data["username"])
            user.password = make_password(form_data["password"], None, "md5")
            user.save()
            created_user = authenticate(username=form_data["username"], password=form_data["password"],)
            login(request, created_user)

            return HttpResponseRedirect("/notes/")
    return render(request, "notes/createUser.html", {"form": form})