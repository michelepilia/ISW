from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect, get_object_or_404
from django.db import models, IntegrityError
from IswBus.models import Biglietto
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from IswBus.models import *
from IswBus.forms import *


'''
    Vista che si occupa di fornire la visualizzazione dei biglietti disponibili
'''
@login_required
def tickets_view(request):
    """A view of all purchasable tickets"""
    tickets = Biglietto.objects.all()
    return render(request, 'available_tickets.html', {'tickets': tickets})


'''
    Vista che si occupa di fornire l'elenco delle ultime transazioni
'''
@login_required
def transactions_view(request):
    """A view of all transactions"""
    transactions = Transazione.objects.filter(utente_id=request.user.id).order_by('data')
    return render(request, 'transactions.html', {'transactions': transactions})


'''
    Vista -> Dettaglio transazione
'''
@login_required
def transaction_detail_view(request, transactionId):
    transaction = Transazione.objects.get(pk=transactionId)
    return render(request, 'transaction_detail.html', {'transaction': transaction, 'ticket': transaction.biglietto})

'''
    Gestione registrazione utente
'''
def signup(request):
    if request.method == 'POST':
        if request.user is not None: #se c'è un utente loggato effettua il logout
            logout(request)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('tickets')
    else:
        if request.user is not None:
            logout(request)
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


'''
    vista-> Aggiunta carta di credito
'''
@login_required
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
            new_card = CartaDiCredito(numero=card_number, mese_scadenza=expiration_month, anno_scadenza=expiration_year,
                                      cvv=cvv, user=user1)
            try:
                new_card.save()
            except IntegrityError: #eccezione che gestisce un eventuale violazione del vincolo unique
                return render_to_response("error.html", {"message": "Carta di credito già esistente"})

            return redirect('/cards/')
    else:
        form = CreditCardForm()
    return render(request, 'add-card.html', {'form': form})

'''
    Vista -> Logout
'''
@login_required
def logout_view(request):
    logout(request)
    # return render(request, 'login.html', {})
    return HttpResponseRedirect('login')


'''
    vista -> Carte disponibili utente
'''
@login_required
def cards(request):
    user = request.user
    cards = CartaDiCredito.objects.filter(user_id=user.id)
    return render(request, "cards.html", {'cards': cards})


'''
    Vista per modificare una carta
'''
@login_required
def edit_card(request, cardId):
    card = CartaDiCredito.objects.get(pk=cardId)
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            expiration_month = form.cleaned_data['expiration_month']
            expiration_year = form.cleaned_data['expiration_year']
            cvv = form.cleaned_data['cvv']
            try:
                card.numero = card_number
                card.mese_scadenza = expiration_month
                card.anno_scadenza = expiration_year
                card.cvv = cvv
                card.pk = cardId
                card.save(force_update=True)
            except IntegrityError:
                return render_to_response("error.html", {"message": "Carta di credito già esistente"})
            return redirect('/cards/')

    else:
        form = CreditCardForm(initial={'card_number': card.numero,
                                       'expiration_month': card.mese_scadenza,
                                       'expiration_year': card.anno_scadenza,
                                       'cvv': card.cvv})
    return render(request, 'edit-card.html', {'form': form, 'card': card})



'''
    Vista acquisto bigliettib
'''
@login_required
def buy_ticket_view(request, ticketId):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    ticket = Biglietto.objects.get(pk=ticketId)
    if request.method == 'POST':
        form = BuyTicketForm(request, request.POST)
        if form.is_valid():
            card = form.cleaned_data['carta']
            try:
                transazione = Transazione(data=timezone.now(), costo=ticket.costo, biglietto=ticket, utente=user,
                                          cartaDiCredito=card)
                transazione.save()
            except IntegrityError:
                return render_to_response("error.html", {"message": "Errore transazione"})
            return redirect('/transactions/')

    else:
        form = BuyTicketForm(request)
    return render(request, 'buy-ticket.html', {'form': form, 'ticket': ticket})

'''
    Vista statistiche acquisti
'''
def statistic_view(request):
    n = 30
    a_month_ago = datetime.now() - timedelta(days=n)

    transactions = Transazione.objects.filter(data__gte=a_month_ago, utente_id=request.user.id)
    number = transactions.count()
    total = 0
    for transaction in transactions:
        total += transaction.costo
    most_purchased = dict(models.tipo_biglietto).get(count_most_purchased(transactions))

    return render(request, 'statistics.html', {'number': number, 'total': total, 'most_purchased': most_purchased})

'''
    Funzione per calcolare il tipo di biglietto più acquistato
'''
def count_most_purchased(transactions):
    uno = 0
    due = 0
    tre = 0
    quattro = 0
    cinque = 0
    for transaction in transactions:
        tipo = transaction.biglietto.tipologia
        if tipo == "1":
            uno += 1
        if tipo == "2":
            due += 1
        if tipo == "3":
            tre += 1
        if tipo == "4":
            quattro += 1
        if tipo == "5":
            cinque += 1
    highest = max(uno, due, tre, quattro, cinque)
    if highest == uno:
        return "1"
    if highest == due:
        return "2"
    if highest == tre:
        return "3"
    if highest == quattro:
        return "4"
    if highest == cinque:
        return "5"

'''
    Se esiste un utente loggato effettua il logout prima di reindirizzare alla vista auth.view.login
'''
def login(request):
    if request.user is not None:
        logout(request)
        return redirect('/auth_login/')
    else:
        return redirect('/auth_login/')
