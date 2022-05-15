from . import views
from django.urls import path

app_name = 'payments'

urlpatterns = [
    path('razorpay/', views.payments, name='payment'),
]