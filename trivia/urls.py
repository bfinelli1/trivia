from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('random', views.random, name='random'),
    path("newgroup", views.newgroup, name="newgroup"),
    path("joingroup/<int:groupid>", views.joingroup, name="joingroup")
]