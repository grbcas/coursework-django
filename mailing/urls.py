from django.urls import path
from django.views.decorators.cache import never_cache

from mailing.apps import MailingConfig
from mailing.views import MailingListView, HomeView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = MailingConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailing_list/', MailingListView.as_view(), name='list'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', never_cache(MailingUpdateView.as_view()), name='edit'),
    path('delete/<int:pk>/', never_cache(MailingDeleteView.as_view()), name='delete'),
]
