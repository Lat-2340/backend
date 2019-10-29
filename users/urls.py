from django.urls import path
from .views import RegisterView
from rest_framework.authtoken import views as AuthViews

urlpatterns = [
  path('register/', RegisterView.as_view()),
  path('auth-token/', AuthViews.obtain_auth_token),
]