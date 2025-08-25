from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('payment/<int:booking_id>/', views.fake_payment, name='fake_payment'),
]
