from django.contrib import admin

# Register your models here.
from mailing.models import Mailing, Client

admin.site.register(Mailing)
admin.site.register(Client)
