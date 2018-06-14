from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.urls import reverse
from django.utils import timezone

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

    def __unicode__(self):
        return "Carta di Credito %s; Scadenza: %d/%d" % (self.numero, self.mese_scadenza, self.anno_scadenza)

class Utente(models.Model):
    nome = models.CharField("Nome", max_length=50)
    cognome = models.CharField("Cognome", max_length=50)
    username = models.CharField("Username", max_length=50)
    password = models.CharField("Password", max_length=50)
    cartaCredito = models.ForeignKey(CartaDiCredito, on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return "%s %s (%s)" % (self.nome, self.cognome, self.username)

class Biglietto(models.Model):
    nome = models.CharField('Nome Biglietto', max_length=50)
    validitaGiorni = models.SmallIntegerField('Giorni di validità')
    costo = models.DecimalField('Costo Biglietto', max_digits=5, decimal_places=2, default=1.50)
    tipologia = models.CharField('Tipo Biglietto', choices=tipo_biglietto, max_length=2)

    def __unicode__(self):
        return "%s (Tipo: %s, Validita: %d giorni) Prezzo: %d €" %(self.nome, self.tipologia, self.validitaGiorni, self.costo)

    def get_url(self):
        return reverse('buy-ticket', args=[str(self.id)])

class Transazione(models.Model):
    data = models.DateTimeField ('Data Acquisto', default=timezone.now)
    costo = models.DecimalField('Totale Transazione', max_digits=5, decimal_places=2)
    biglietto = models.ForeignKey(Biglietto, on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return "%s, %s, %d" % (self.data, self.biglietto, self.costo)