from django.contrib import admin
from .models import ContactResponse, Stocks
# Register your models here.


@admin.register(ContactResponse)
class ContactResponseAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_on')


@admin.register(Stocks)
class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_name', 'stock_url')