from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from IswBus.models import Biglietto
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from IswBus.forms import *


from IswBus.models import *
from IswBus.forms import *


@login_required()
def tickets_view(request):
    """A view of all purchasable tickets"""
    tickets = Biglietto.objects.all()
    return render(request, 'available_tickets.html', {'tickets':tickets})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        user_form = UserForm(request.POST)
        add_card_form = CreditCardForm(request.POST)
        if (form.is_valid() and user_form.is_valid() and add_card_form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            nome = user_form.cleaned_data['nome']
            cognome = user_form.cleaned_data['cognome']
            card_number = add_card_form.cleaned_data['card_number']
            expiration_month = add_card_form.cleaned_data['expiration_month']
            expiration_year = add_card_form.cleaned_data['expiration_year']
            cvv = add_card_form.cleaned_data['cvv']
            login(request, user)
            sub_user = Utente(django_user=user, nome=nome, cognome=cognome)
            credit_card = CartaDiCredito(numero=card_number, mese_scadenza=expiration_month, anno_scadenza=expiration_year, cvv=cvv, user=sub_user)
            sub_user.save()
            credit_card.save()


            return redirect('tickets')
    else:
        form = UserCreationForm()
        user_form = UserForm()
        add_card_form = CreditCardForm()


    return render(request, 'signup.html', {'form': form, 'user_form': user_form, 'add_card_form':add_card_form})

@login_required
def paymentTransactionView(request, ticketId):
    try:
        ticket = Biglietto.objects.get(pk=ticketId)
    except Biglietto.DoesNotExist:
        ticket = None

    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            card = CartaDiCredito()
            card.numero = form.cleaned_data['card_number']
            card.anno_scadenza = form.cleaned_data['expiration_year']
            card.mese_scadenza = form.cleaned_data['expiration_month']
            card.cvv = form.cleaned_data['cvv']
            card.save()
            transaction = Transazione(data=timezone.now, costo=ticket.costo, biglietto=ticket, utente=request.user, cartaDiCredito=card)
            transaction.save()
        return HttpResponse("Transaction saved!!")
    else:
        form = CreditCardForm()

    return render(request, "buy-ticket.html", {'form': form})