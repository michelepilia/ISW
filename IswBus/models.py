from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.utils.deconstruct import deconstructible

'''
    Tuple relative al tipo di biglietto
'''
tipo_biglietto = (
    ('1', 'Abbonamento Mensile'),
    ('2', 'Corsa singola 90 minuti'),
    ('3', 'Biglietto 12 Corse'),
    ('4', 'Corsa singola integrata 120 minuti'),
    ('5', 'Abbonamento annuale'),
)


'''
    Classe carta di credito
'''
@deconstructible
class CartaDiCredito(models.Model):
    numero = models.CharField("Numero Carta di Credito", max_length=16, default="1111222233334444", unique=True)
    mese_scadenza = models.SmallIntegerField("Mese di Scadenza", default=datetime.now().month)
    anno_scadenza = models.SmallIntegerField("Anno di Scadenza", default=datetime.now().year)
    cvv = models.CharField("Codice CVV", max_length=3, default="123")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def get_full_name(self):
        return "Carta di Credito %s (Scadenza: %d/%d)" % (self.numero, self.mese_scadenza, self.anno_scadenza)

    def get_url(self):
        return reverse('edit-card', args=[str(self.id)])

'''
    Classe biglietto
'''
@deconstructible
class Biglietto(models.Model):
    nome = models.CharField('Nome Biglietto', max_length=50, default="Name")
    validitaGiorni = models.SmallIntegerField('Giorni di validità', default=7)
    costo = models.DecimalField('Costo Biglietto', max_digits=5, decimal_places=2, default=1.50)
    tipologia = models.CharField('Tipo Biglietto', choices=tipo_biglietto, max_length=2, default="1")

    def get_full_name(self):
        return "%s (Tipo: %s, Validita: %d giorni) Prezzo: %.2f €" % (
            self.nome, dict(tipo_biglietto)[self.tipologia], self.validitaGiorni, self.costo)

    def get_url(self):
        return reverse('buy-ticket', args=[str(self.id)])


'''
    Classe relativa alle transazioni
'''
@deconstructible
class Transazione(models.Model):
    data = models.DateTimeField('Data Acquisto', default=timezone.now)
    costo = models.DecimalField('Totale Transazione', max_digits=5, decimal_places=2, default=1.30)
    biglietto = models.ForeignKey(Biglietto, on_delete=models.DO_NOTHING, default=Biglietto())
    utente = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    cartaDiCredito = models.ForeignKey(CartaDiCredito, on_delete=models.DO_NOTHING, default=CartaDiCredito())

    def get_full_name(self):
        return "%s, %s, %d" % (self.data, self.biglietto, self.costo)

    def get_url(self):
        return reverse('transaction', args=[str(self.id)])