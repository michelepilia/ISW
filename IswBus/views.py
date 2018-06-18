from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect, get_object_or_404
from django.db import models, IntegrityError
from IswBus.models import Biglietto
from django.contrib.auth import login, authenticate, logout
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


@login_required
def add_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        print("is valid?")
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            expiration_month = form.cleaned_data['expiration_month']
            expiration_year = form.cleaned_data['expiration_year']
            cvv = form.cleaned_data['cvv']
            if request.user.is_authenticated:
                user1 = request.user
            else:
                user1 = None
            new_card = CartaDiCredito(numero=card_number, mese_scadenza=expiration_month, anno_scadenza=expiration_year,
                                      cvv=cvv, user=user1)
            try:
                new_card.save()
            except IntegrityError:
                return render_to_response("error.html", {"message": "Carta di credito già esistente"})

            return redirect('/cards/')
    else:
        print("else pre")
        form = CreditCardForm()
        print("else post")
    return render(request, 'add-card.html', {'form': form})


@login_required
def logout_view(request):
    print(1)
    logout(request)
    print(2)
    # return render(request, 'login.html', {})
    return HttpResponseRedirect('login')


def cards(request):
    user = request.user
    cards = CartaDiCredito.objects.filter(user_id=user.id)
    return render(request, "cards.html", {'cards': cards})


@login_required
def edit_card(request, cardId):
    card = CartaDiCredito.objects.get(pk=cardId)
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        print("is it valid?")
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            expiration_month = form.cleaned_data['expiration_month']
            expiration_year = form.cleaned_data['expiration_year']
            cvv = form.cleaned_data['cvv']
            try:
                card.numero=card_number
                card.mese_scadenza=expiration_month
                card.anno_scadenza=expiration_year
                card.cvv=cvv
                card.pk=cardId
                card.save(force_update=True)
                print("FATTO!!!!")
            except IntegrityError:
                return render_to_response("error.html", {"message": "Carta di credito già esistente"})
            return redirect('/cards/')

    else:
        print("else it pre")
        form = CreditCardForm(initial={'card_number': card.numero,
                                       'expiration_month': card.mese_scadenza,
                                       'expiration_year': card.anno_scadenza,
                                       'cvv': card.cvv})
        print("else it post")
    return render(request, 'edit-card.html', {'form': form, 'card': card})


@login_required
def buy_ticket_view(request, ticketId):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    ticket = Biglietto.objects.get(pk=ticketId)
    if request.method == 'POST':
        form = BuyTicketForm(request.POST, initial={'carta':CartaDiCredito.objects.filter(user_id=request.user.id)})
        if form.is_valid():
            card = form.cleaned_data['carta']
            try:
                Transazione(data=timezone.now, costo=ticket.costo, biglietto=ticket, utente=user, cartaDiCredito=card)
            except IntegrityError:
                return render_to_response("error.html", {"message": "Errore transazione"})
            return redirect('/cards/')

    else:
        print("else it pre")
        form = BuyTicketForm(initial={'carta':CartaDiCredito.objects.filter(user_id=request.user.id)})
        print("else it post")
    return render(request, 'buy-ticket.html', {'form': form, 'ticket': ticket})