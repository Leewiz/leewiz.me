from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    # ex: /
    path("", views.IndexView.as_view(), name="index"),
]