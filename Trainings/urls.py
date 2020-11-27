from django.urls import path
from . import views

app_name = 'Trainings'
urlpatterns=[
    path('trainings/allusers/<int:pk>/create_skills', views.Create_Skills.as_view(), name='Create_User_Skills'),
    path('trainings/allusers/<int:pk>/delete_skills', views.Skills_Delete.as_view(), name='Delete_User_Skills'),
    path('trainings/allusers/<int:pk>/update_skills', views.Update_Skills.as_view(), name='Update_User_Skills'),
    path('trainingslist/', views.hyperlink_training_courses, name='hyperlink_training_list'),
]