from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("predict/", views.predict_view, name="predict"),
    path("about/", views.about_view, name="about"),
]
