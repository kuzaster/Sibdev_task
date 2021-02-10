from django.contrib import admin
from django.urls import path, include
from .views import CustomersView
# app_name = "sibdevapp"

urlpatterns = [
    path('deals/', CustomersView.as_view())
]
