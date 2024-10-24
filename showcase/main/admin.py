from django.contrib import admin
from .models import ContactResponse
# Register your models here.


@admin.register(ContactResponse)
class ContactResponseAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_on')
