from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from IswBus.models import Biglietto

from IswBus.models import Biglietto

def tickets_view(request):
    """A view of all purchasable tickets"""
    tickets=Biglietto.objects.all()
    return render(request, 'available_tickets.html', {'tickets':tickets})
