
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from mailing import services
from mailing.forms import MailingForm
from mailing.models import Mailing
from mailing.services import send_mailing, get_user_statistic


class HomeView(TemplateView):
    """
    Класс-контроллер для отображения домашней страницы.
    """
    model = Mailing
    template_name = 'mailing/home.html'
    extra_context = {
        'total_mailings': len(model.objects.all()),
        'active_mailings': 1,
        'clients': model.objects.all()
    }

    # def get_context_data(self, **kwargs) -> dict:
    #     """
    #     Вывод статистики рассылок
    #     """
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     if user.is_authenticated:
    #         user_statistic = services.get_user_statistic(user)
    #         context.update(user_statistic)
    #     return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Форма создания рассылки
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')


def send_mailing_btn(request, pk):
    """вызвать сервис метод POST"""

    print(f'send_mailing:{request.POST}')
    # send_mailing()
    return redirect('mailing_list/')


def toggle_status_mailing(request, pk):
    """
    Контроллер деактивации рассылки.
    """
    print(f'toggle status mailing:{request.POST}')
    if request.POST:
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.status_stop = 1
        mailing.status_run = 0
        mailing.save()

    return redirect('mailing_list/')
