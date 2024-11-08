from django.urls import path
from . import views
from .views import get_stock

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
    
    # stocks
    path('get-stocks', views.get_stock, name='get_stock'),
    path('get-meta-stocks', views.get_meta_stock, name='get_meta_stock'),
    path('stocks', views.stocks, name='stocks'),
    path('stock/<int:id>/', views.fetch_stock_price, name='fetch_stock_price'),

]