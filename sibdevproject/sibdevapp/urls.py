from django.urls import path

from .views import CustomersView

urlpatterns = [path("deals/", CustomersView.as_view(), name="get_post_deals")]
