"""IswBus URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from IswBus import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tickets/', views.tickets_view, name='tickets'),
    url(r'^$', auth_views.login, name='login'),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^ticket/(?P<ticketId>\d+)/', views.buy_ticket_view, name="buy-ticket"),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^add_card/', views.add_card, name='add-card'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^cards/', views.cards, name='manage-card'),
    url(r'^edit-card/(?P<cardId>\d+)/', views.edit_card, name="edit-card"),
    url(r'^transactions/', views.transactions_view, name="transactions"),
    url(r'^transaction/(?P<transactionId>\d+)/', views.transaction_detail_view, name="transaction"),
    url(r'^statistics/', views.statistic_view, name="statistics"),
]