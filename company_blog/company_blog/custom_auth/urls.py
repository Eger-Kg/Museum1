from django.urls import path, re_path
from .views import register, activate


urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>', activate, name='activate')
]