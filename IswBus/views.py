from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.db import models, IntegrityError
from IswBus.models import Biglietto
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from IswBus.models import *
from IswBus.forms import *


@login_required
def tickets_view(request):
    """A view of all purchasable tickets"""
    tickets = Biglietto.objects.all()
    return render(request, 'available_tickets.html', {'tickets': tickets})


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


def buy_ticket(request, ticketId):
    ticket = Biglietto.objects.get(pk=ticketId)
    return render(request, 'buy-ticket.html', {'ticket': ticket})


def add_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            expiration_month = form.cleaned_data['expiration_month']
            expiration_year = form.cleaned_data['expiration_year']
            cvv = form.cleaned_data['cvv']
            if request.user.is_authenticated:
                user1 = request.user
            else:
                user1 = None
            new_card = CartaDiCredito(numero=card_number, mese_scadenza=expiration_month, anno_scadenza=expiration_year, cvv=cvv, user=user1)
            try:
                new_card.save()
            except IntegrityError:
                return render_to_response("error.html", {"message": "Carta di credito già esistente"})

            return redirect('tickets')
    else:
        form = CreditCardForm()
    return render(request, 'add-card.html', {'form': form})
