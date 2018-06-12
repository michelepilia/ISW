from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.urls import reverse
import datetime

tipo_biglietto = (
        ('1', 'Abbonamento Mensile'),
        ('2', 'Corsa singola 90 minuti'),
        ('3', 'Biglietto 12 Corse'),
        ('4', 'Corsa singola integrata 120 minuti'),
        ('5', 'Abbonamento annuale'),
    )


class CartaDiCredito(models.Model):
    numero = models.CharField("Numero Carta di Credito", max_length=16)
    mese_scadenza = models.SmallIntegerField("Mese di Scadenza")
    anno_scadenza = models.SmallIntegerField("Anno di Scadenza")
    cvv = models.CharField("Codice CVV", max_length=3)

class Utente(models.Model):
    username = models.CharField("Username", max_length=50)
    password = models.CharField("Password", max_length=50)
    cartaCredito = models.ForeignKey ("Carta di Credito", CartaDiCredito)


class Biglietto(models.Model):
    nome = models.CharField('Nome Biglietto', max_length=50)
    validitaGiorni = models.SmallIntegerField('Giorni di validità')
    costo = models.DecimalField('Costo Biglietto', max_digits=5, decimal_places=2, default=1.50)
    tipologia = models.CharField('Tipo Biglietto', choices=tipo_biglietto)

class Transazione(models.Model):
    data = models.DateTimeField ('Data Acquisto', default=datetime.datetime.now())
    costo = models.DecimalField('Totale Transazione', max_digits=5, decimal_places=2)
    tipo = models.CharField('Tipo Biglietto', choices=tipo_biglietto)