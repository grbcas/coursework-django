from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.form import MailingForm
from mailing.models import Mailing


class HomeView(ListView):
    """
    Класс-контроллер для отображения домашней страницы.
    """
    model = Mailing
    template_name = 'mailing/home.html'


class MailingListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    """
    Форма создания рассылки
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')


class MailingDeleteView(DeleteView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')