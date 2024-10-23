from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('sign-up', views.signup, name="signup"),
    path('sign-in', views.signin, name="signin"),
    path('sign-out', views.signout, name="signout"),
]