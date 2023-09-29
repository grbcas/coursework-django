from django.shortcuts import render
from django.views.generic import ListView
from mailing.models import Mailing


class MailingListView(ListView):
    model = Mailing
