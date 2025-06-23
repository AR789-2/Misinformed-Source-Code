from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("name/", views.name, name="name"),
    path("win/", views.win, name="win"),
    path("loss/", views.loss, name="loss"),
    path("shop/", views.upgrade, name="upgrade"),
    path("rep/<int:rep>/<int:profit>", views.SETREPUTATION, name="reputation"),
    path("shop/<str:upg_id>", views.purchase, name="purchase")
]