
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from mailing import services
from mailing.forms import MailingForm
from mailing.models import Mailing, Client, Message
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

    # def get_object(self, queryset=None):
    #     return self.request.user

    def get_context_data(self, **kwargs) -> dict:
        """
        Вывод статистики рассылок
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        Client.objects.filter(owner=self.request.user) # working case
        print(user)
        if user.is_authenticated:
            user_statistic = services.get_user_statistic(user)
            context.update(user_statistic)
        return context


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
    return redirect('mailing:list')


def toggle_status_mailing(request, pk):
    """
    Контроллер деактивации рассылки.
    """
    # print(f'toggle status mailing:{request.POST}')
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.status_stop = 1
    mailing.status_run = 0
    mailing.save()

    # return redirect('mailing_list/') # как-то тоже работало, вопрос почему и как?
    return redirect('mailing:list')


# GPT code
@require_POST
def create_message(request):
    if request.method == 'POST':
        try:
            text = request.POST['text']
            message = Message(text=text)
            message.save()
            return HttpResponse('Сообщение создано!')
        except KeyError as e:
            return HttpResponseBadRequest('Ошибка: {}'.format(e))
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))
