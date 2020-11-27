from django.urls import path,include
from rest_framework import routers
from .api import LoginViewSet
# from django.contrib.auth import view as auth_views

from .views import (login_page)

router = routers.DefaultRouter()
router.register('api/', LoginViewSet, 'Loggins')

app_name = ''

urlpatterns = [
    path('', login_page, name ="login-page")
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name="rest_password")
    # path('',include(django.contrib.auth.views))
]
