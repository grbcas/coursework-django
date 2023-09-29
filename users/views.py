import os

from django.contrib.auth.views import (PasswordResetDoneView as BasePasswordResetDoneView,
                                       PasswordResetView as BasePasswordResetView,
                                       PasswordResetConfirmView as BasePasswordResetConfirmView,
                                       PasswordResetCompleteView as BasePasswordResetCompleteView)

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail

from config import settings
from users.forms import UserForm, UserProfileForm, VerificationForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    queryset = User.objects.last()

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.set_unusable_password()
            new_user.save()

            # Send an email to the user with the token:

            current_site = get_current_site(self.request)
            print('current_site', current_site)

            verification_key = urlsafe_base64_encode(force_bytes(new_user.pk))

            print('RegisterView: verification_key', verification_key, 'new_user.pk', new_user.pk)
            url = f'http://{current_site}/users/verification?verification_key={verification_key}\n'

            send_mail(
                subject='Верификация почты',
                message=f'перейдите по ссылке: {url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[new_user.email]
            )

        return super().form_valid(form)


def verification(request):
    key_data = request.GET.get('verification_key')
    template = 'users/verification.html'
    verification_key = int(urlsafe_base64_decode(key_data).decode())
    print(key_data, '=', verification_key)
    user = User.objects.get(pk=verification_key)

    if request.method == 'POST':
        form = VerificationForm(request.POST)  # or None)
        if form.is_valid():
            # user = User.objects.get(pk=verification_key)
            user.is_verified = True
            user.is_active = True
            user.save()
            return redirect(reverse('catalog:index'))
    form = VerificationForm(request.POST or None)
    context = {'form': form, 'user_email': user.email}
    return render(request, template, context)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordView(PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(BasePasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    success_url = reverse_lazy('users:password_reset_done')


class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    success_url = reverse_lazy('users:login')
