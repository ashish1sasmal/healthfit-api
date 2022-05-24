from . import views
from django.urls import path

urlpatterns = [
    path("register", views.doctorRegister, name="doctorRegister"),
    path("search/", views.searchData, name="search"),
    path("add/", views.addDoctor),
    path("<str:doc_id>/", views.getDoctor, name="get_doctor"),
    path("dashboard/<str:doc_id>", views.getDashboard),
    path("update/<str:doc_id>/", views.updateDocStatus)
]
