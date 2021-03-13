from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify-account/', views.EmailVerify.as_view(), name='email_verify')
    ]