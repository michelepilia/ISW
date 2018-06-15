from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from IswBus.models import Biglietto

from IswBus.models import *
from IswBus.forms import *

def tickets_view(request):
    """A view of all purchasable tickets"""
    tickets=Biglietto.objects.all()
    return render(request, 'available_tickets.html', {'tickets':tickets})

def buy_ticket(request, ticketId):
    try:
        ticket = Biglietto.objects.get(pk=ticketId)
    except Biglietto.DoesNotExist:
        book = None

    #if request.method == "POST":
        current_user = request.user
        creditForm = CreditCardForm(request.POST)
        #if CreditCardForm.is_valid():
         #   newCardForm = CreditCardForm(numero=CreditCardForm.cleaned_data['author_name'],
          #                     mese_scadenza=CreditCardForm.cleaned_data['author_surname'],
                                        #)
           # newCardForm.save()
          #  return HttpResponse("Author saved!!")
    #else:
        #newCardForm = CreditCardForm()

    return render(request,
                  "buy-ticket.html",
                  {
                      'ticket': ticket,
                      'ticketId': ticketId,
                      #'form': newCardForm
                  })