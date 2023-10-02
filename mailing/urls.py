from django.urls import path
from django.views.decorators.cache import never_cache

from mailing.apps import MailingConfig
from mailing.views import MailingListView, HomeView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    toggle_status_mailing, send_mailing_btn

app_name = MailingConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailing_list/', MailingListView.as_view(), name='list'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', never_cache(MailingUpdateView.as_view()), name='edit'),
    path('delete/<int:pk>/', never_cache(MailingDeleteView.as_view()), name='delete'),
    path('<int:pk>', toggle_status_mailing, name='toggle_status_mailing'), # работает через форму
    path('<int:pk>/', send_mailing_btn, name='send_mailing_btn'), # work via href
    path('message/', send_mailing_btn, name='send_mailing_btn'),
]