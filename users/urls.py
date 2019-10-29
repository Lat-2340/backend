from django.urls import path
from .views import NewUserView

urlpatterns = [
  path('newuser/', NewUserView.as_view()),
]