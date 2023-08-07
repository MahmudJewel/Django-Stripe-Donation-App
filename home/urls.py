from django.urls import path, include
from .views import home, stripePay, paysuccess

urlpatterns = [
    # path('', home, name='home'),
    path('', stripePay, name="main_home"),
    path('pay_success/', paysuccess, name="success_page"),
] 