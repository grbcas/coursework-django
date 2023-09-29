from django.urls import path, include

from mailing.apps import MailingConfig
from mailing.views import MailingListView

app_name = MailingConfig.name


urlpatterns = [
    path('home', MailingListView.as_view(), name='home'),
]
