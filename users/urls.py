from django.urls import path
from .views import NewUserView
from rest_framework.authtoken import views as AuthViews

urlpatterns = [
  path('new-user/', NewUserView.as_view()),
  path('auth-token/', AuthViews.obtain_auth_token),
]