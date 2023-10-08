
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import Form
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from blog.models import Blog
from mailing import services
from mailing.forms import MailingForm, ClientForm
from mailing.models import Mailing, Client, Message
from mailing.services import manual_send_mailing


class HomeView(TemplateView):
    """
    Класс-контроллер для отображения домашней страницы.
    """
    model = Mailing
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['object_list'] = Blog.objects.order_by('?')[:3]
        if user.is_authenticated:
            user_statistic = services.get_user_statistic(user)
            context.update(user_statistic)

        return context


class OwnerSuperuserMixin:
    """
    Миксин, ограничивающий демонстрацию страницы объекта для пользователя,
    который не является ни владельцем объекта, ни суперюзером
    """

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MailingListView(LoginRequiredMixin, OwnerSuperuserMixin, ListView):
    model = Mailing

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        is_manager = user.groups.filter(name='Managers').exists()
        if user.is_superuser or is_manager:
            queryset = super().get_queryset().all()
        else:
            queryset = super().get_queryset().filter(owner=user)
        return queryset.order_by('name')


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Форма создания рассылки
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')


class MailingUpdateView(LoginRequiredMixin, OwnerSuperuserMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('subject', 'body', 'owner')
    success_url = reverse_lazy('mailing:list_message')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ('subject', 'body', 'owner')
    success_url = reverse_lazy('mailing:list_message')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:list_message')


def send_mailing_btn(request, pk):
    """Контроллер - отправки сообщения клиентам рассылки кнопкой Send"""
    print(f'send_mailing {pk}')
    manual_send_mailing(pk)
    return redirect('mailing:list')


def toggle_status_mailing(request, pk):
    """
    Контроллер деактивации рассылки.
    """
    # from request get user if not return 403
    print(f'toggle status mailing')
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.status_stop = 1
    mailing.status_run = 0
    mailing.save()

    return redirect('mailing:list')


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Класс-контроллер для создания клиента (Client)
    """

    model = Client
    template_name = 'mailing/recipient_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:recipients_list')
    extra_context = {
        'title': 'Создать контакт',
        'button': 'Создать',
    }

    def form_valid(self, form: Form) -> HttpResponse:
        """
        Обработка действий при валидности формы.

        Обрабатывает поля ФИО, объединяя их в одно поле name
        """

        last_name = self.request.POST.get('last_name', '').strip()
        first_name = self.request.POST.get('first_name', '').strip()
        father_name = self.request.POST.get('father_name', '').strip()

        full_name = f"{last_name} {first_name} {father_name}".strip().title()

        form.instance.name = full_name

        self.object = form.save()
        self.object.owner = self.request.user

        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """
    Класс-контроллер для отображения списка клиентов.

    Просмотр доступен только авторизованным пользователям.
    Список клиентов зависит от статуса текущего пользователя:
    обычный юзер может видеть только клиентов, которых он создавал,
    менеджер и суперюзер могут видеть весь перечень клиентов,
    существующий в базе данных
    """

    model = Client
    template_name = 'mailing/recipients_list.html'

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        is_manager = user.groups.filter(name='Managers').exists()
        if user.is_superuser or is_manager:
            queryset = super().get_queryset().all()
        else:
            queryset = super().get_queryset().filter(owner=user)
        return queryset.order_by('name')


class ClientUpdateView(LoginRequiredMixin, OwnerSuperuserMixin, UpdateView):
    """
    Класс-контроллер для редактирования клиента (Client).

    Доступ к странице есть либо у создателя этого клиента,
    либо у суперюзера
    """

    model = Client
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients_list')
    form_class = ClientForm

    def get_context_data(self, **kwargs) -> dict:
        """
        Добавление в контекст конкретного объекта модели Client,
        а также надписи в заголовке и на кнопке
        """

        context_data = super().get_context_data(**kwargs)
        extra_context = {
            'object': Client.objects.get(pk=self.kwargs.get('pk')),
            'title': 'Изменить контакт',
            'button': 'Сохранить',
        }
        return context_data | extra_context

    def form_valid(self, form):
        """
        Обработка действий при валидности формы.

        Обрабатывает поля ФИО, объединяя их в одно поле name
        """

        last_name = self.request.POST.get('last_name', '').strip()
        first_name = self.request.POST.get('first_name', '').strip()
        father_name = self.request.POST.get('father_name', '').strip()

        full_name = f"{last_name} {first_name} {father_name}".strip().title()

        form.instance.name = full_name

        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, OwnerSuperuserMixin, DeleteView):
    """
    Класс-контроллер для удаления конкретного клиента
    """

    model = Client
    template_name = 'mailing/recipient_delete.html'
    success_url = reverse_lazy('mailing:recipients_list')

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = Client.objects.get(pk=self.kwargs.get('pk'))
        return context_data
