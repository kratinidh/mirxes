from django.contrib import admin
from .models import Ticket, Ticket_Comments

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Ticket_Comments)
