from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify-account/', views.EmailVerify.as_view(), name='email_verify'),
    path('', include(router.urls))
    ]