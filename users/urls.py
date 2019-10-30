from django.urls import path
from .views import UserRegisterView, TokenDestroyView, getPickupLocationsView
from rest_framework.authtoken import views as AuthViews

urlpatterns = [
  path('register/', UserRegisterView.as_view()),
  path('login/', AuthViews.obtain_auth_token),
  path('logout/', TokenDestroyView.as_view()),
  path('pickup-locations/', getPickupLocationsView, name='pickup-locations')
]