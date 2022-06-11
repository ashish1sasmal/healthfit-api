from django.urls import path
from . import views

app_name = "consult"

urlpatterns = [
    path("payment/<str:apmt_id>", views.payments, name="payment"),
    path("get/all", views.allAppointments),
    path("get/<str:apmt_id>", views.getApmtDetails, name="home"),
    path("save/<str:apmt_id>", views.endConsult),
    path("current", views.currentConsult),
    path("start/", views.startConsult),
    path("update/<str:apmt_id>", views.updateConsult),
    path("upload/", views.uploadFile)
    
]
