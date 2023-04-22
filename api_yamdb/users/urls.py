from django.urls import path

from .views import get_confirmation, get_token

urlpatterns = [
    path('signup/', get_confirmation),
    path('token/', get_token),
]
