from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from IswBus.models import Biglietto
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


from IswBus.models import *
from IswBus.forms import *

@login_required
def tickets_view(request):
    """A view of all purchasable tickets"""
    tickets=Biglietto.objects.all()
    return render(request, 'available_tickets.html', {'tickets':tickets})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('tickets')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})