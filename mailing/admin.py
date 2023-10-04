from django.contrib import admin

# Register your models here.
from mailing.models import Mailing, Client, Message

admin.site.register(Mailing)
admin.site.register(Client)
admin.site.register(Message)