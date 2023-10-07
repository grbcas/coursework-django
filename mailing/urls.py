from django.urls import path
from django.views.decorators.cache import never_cache, cache_page

from mailing.apps import MailingConfig
from mailing.views import MailingListView, HomeView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    toggle_status_mailing, send_mailing_btn, MessageCreateView, MessageListView, MessageDeleteView, MessageUpdateView, \
    ClientCreateView, ClientListView, ClientUpdateView, ClientDeleteView

app_name = MailingConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('mailing_list/', MailingListView.as_view(), name='list'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', never_cache(MailingUpdateView.as_view()), name='edit'),
    path('delete/<int:pk>/', never_cache(MailingDeleteView.as_view()), name='delete'),

    path('<int:pk>', toggle_status_mailing, name='toggle_status_mailing'), # работает через форму
    path('<int:pk>/', send_mailing_btn, name='send_mailing_btn'), # work via href

    path('message/create/', MessageCreateView.as_view(), name='create_message'),
    path('message/list/', MessageListView.as_view(), name='list_message'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
    path('message/edit/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),

    path('new_recipient/', ClientCreateView.as_view(), name='new_recipient'),
    path('recipients_list/', cache_page(60)(ClientListView.as_view()), name='recipients_list'),
    path('<int:pk>/update_recipient/', ClientUpdateView.as_view(), name='update_recipient'),
    path('<int:pk>/delete_recipient/', ClientDeleteView.as_view(), name='delete_recipient'),
]