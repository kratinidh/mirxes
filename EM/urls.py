from django.urls import path

from . import views

app_name = 'EM'
urlpatterns=[
    path('HR/', views.HR_EM, name = 'HR_EM'),
    path('HRM/', views.HRM_EM, name = 'HRM_EM'),

    path('HR/create_profiles/', views.Create_Profile.as_view(), name ='Create_Profile'),

    path('HR/<int:pk>/', views.Profile_View.as_view(), name ='Detail_Profile'),
    path('HR/<int:pk>/DeleteP', views.Delete_Profile.as_view(),name='Delete_Profile'),
    path('HR/<int:pk>/UpdateP', views.Update_Profile.as_view(), name ='Update_Profile')
]