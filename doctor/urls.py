from . import views
from django.urls import path

urlpatterns = [
    path('register', views.doctorRegister, name='doctorRegister'),
    path('', views.getDoctors, name="get_doctors"),
    path('search/', views.searchData, name="search")
]