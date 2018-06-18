# Generated by Django 2.0.6 on 2018-06-18 07:57

import IswBus.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Biglietto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='Name', max_length=50, verbose_name='Nome Biglietto')),
                ('validitaGiorni', models.SmallIntegerField(default=7, verbose_name='Giorni di validità')),
                ('costo', models.DecimalField(decimal_places=2, default=1.5, max_digits=5, verbose_name='Costo Biglietto')),
                ('tipologia', models.CharField(choices=[('1', 'Abbonamento Mensile'), ('2', 'Corsa singola 90 minuti'), ('3', 'Biglietto 12 Corse'), ('4', 'Corsa singola integrata 120 minuti'), ('5', 'Abbonamento annuale')], default='1', max_length=2, verbose_name='Tipo Biglietto')),
            ],
        ),
        migrations.CreateModel(
            name='CartaDiCredito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(default='1111222233334444', max_length=16, unique=True, verbose_name='Numero Carta di Credito')),
                ('mese_scadenza', models.SmallIntegerField(default=6, verbose_name='Mese di Scadenza')),
                ('anno_scadenza', models.SmallIntegerField(default=2018, verbose_name='Anno di Scadenza')),
                ('cvv', models.CharField(default='123', max_length=3, verbose_name='Codice CVV')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transazione',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data Acquisto')),
                ('costo', models.DecimalField(decimal_places=2, default=1.3, max_digits=5, verbose_name='Totale Transazione')),
                ('biglietto', models.ForeignKey(default=IswBus.models.Biglietto(), on_delete=django.db.models.deletion.DO_NOTHING, to='IswBus.Biglietto')),
                ('cartaDiCredito', models.ForeignKey(default=IswBus.models.CartaDiCredito(), on_delete=django.db.models.deletion.DO_NOTHING, to='IswBus.CartaDiCredito')),
                ('utente', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
