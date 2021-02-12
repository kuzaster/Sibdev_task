from django.contrib import admin

from .models import Customer, Deals

admin.site.register(Deals)
admin.site.register(Customer)
# Register your models here.
