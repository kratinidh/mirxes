from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('userhome/', views.user_dashboard, name='user_homepage'),
    path('managerhome/', views.manager_dashboard, name='manager_homepage'),
    path('hrhome/', views.HR_dashboard, name='hr_homepage'),
    path('hrmanagerhome/', views.HRmanager_dashboard, name='hrmanager_homepage'),

    path('profile/Create', views.Create_Profile, name='Create_Profile'),
    path('profile/Bulkcreate', views.Profile_Upload, name='BulkCreate_Profile'),

    path('profile/all/<int:pk>/Update', views.Update_Profile, name='UpdateProfilepage'),
    path('profile/HRM/<int:pk>/Update', views.Update_Profile_HR, name='HRM_UpdateProfilepage'),

    path('profile/all/<int:pk>', views.Detail_Profile, name='Detail_Profile'),
    path('profile/HRM/<int:pk>', views.Detail_Profile_HR, name='Detail_Profile_HR'),

    path('profile/all/<int:pk>/CreateQualifications', views.Create_Qualifications.as_view(),
         name='Create_Qualifications'),
    path('profile/all/<int:pk>/<int:mk>/DeleteQualifications', views.Delete_Qualifications.as_view(),
         name='Delete_Qualifications'),

    path('profile/HRM/<int:pk>/CreateQualifications', views.Create_Qualifications_HR.as_view(),
         name='HRM_Create_Qualifications'),
    path('profile/HRM/<int:pk>/<int:mk>/DeleteQualifications', views.Delete_Qualifications_HR.as_view(),
         name='HRM_Delete_Qualifications'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="login2/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="login2/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="login2/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="login2/password_reset_done.html"),
         name="password_reset_complete"),
]
