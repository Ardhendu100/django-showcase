from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    
    path('send_otp', views.send_otp, name='send_otp'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('sign-up', views.signup, name="signup"),
    path('sign-in', views.signin, name="signin"),
    path('sign-out', views.signout, name="signout"),
    
    path('contact-us', views.contactus, name="contactus"),
    path('chatbot', views.chatbot, name="chatbot"),
    
    # users
    path('users', views.users, name='users'),
    

]