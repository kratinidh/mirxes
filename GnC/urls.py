from django.urls import path

from . import views
from .views import User_GnC, Manager_GnC,  Create_Departmental_Goals, Create_Competencies, Create_Departmental_Competencies

app_name = 'GnC'
urlpatterns = [
    path('user/', views.User_GnC, name = "User_GnC"),
    path('manager/', views.Manager_GnC, name = "Manager_GnC"),
    path('HR/', views.HR_GnC, name = "HR_GnC"),
    
    path('allusers/<int:pk>/create_departmental_goals/', views.Create_Departmental_Goals.as_view(), name = "Create_Manager_Goals"),
    path('allusers/<int:pk>/create_departmental_competencies/', views.Create_Departmental_Competencies.as_view(), name="Create_Manager_Competencies"),
    path('allusers/<int:pk>/create_goals/', views.Create_Goals.as_view(), name ="Create_User_Goals1"),
    path('allusers/<int:pk>/create_competencies/', views.Create_Competencies.as_view(), name = "Create_User_Competencies"),
    path('allusers/<int:pk>/create_KPI/', views.Create_KPI.as_view(), name = "Create_User_KPIs"),
    path('allusers/<int:pk>/UserGnC/Create_GoalsCom', views.Create_Goals_Comments.as_view(), name='Create_User_Goals_Comments'),
    path('allusers/<int:pk>/UserGnC/Create_CompetenciesCom', views.Create_Competencies_Comments.as_view(), name ='Create_User_Competencies_Comments'),

    path('allusers/<int:pk>/DepartmentG', views.Departmental_Goals_View.as_view(), name="Detail_Departmental_Goals"),
    path('allusers/<int:pk>/UserG', views.Goals_View.as_view(), name = "Detail_Goals"),
    path('allusers/<int:pk>/UserC', views.Competencies_View.as_view(), name="Detail_Competencies"),
    path('allusers/<int:pk>/UserGnC', views.Department_View.as_view(), name="Detail_Users"),
    path('allusers/<int:pk>/Departments', views.HRDepartment_view.as_view(), name="Detail_Departments"),

    path('allusers/<int:pk>/DeleteG', views.Goals_Delete.as_view(), name = "Delete_User_Goals"),
    path('allusers/<int:pk>/DeleteDepartmentalG', views.Departmental_Goals_Delete.as_view(), name ="Delete_Departmental_Goals"),
    path('allusers/<int:pk>/DeleteDepartmentalC', views.Departmental_Competencies_Delete.as_view(), name="Delete_Departmental_Competencies"),
    path('allusers/<int:pk>/DeleteC', views.Competencies_Delete.as_view(), name ="Delete_User_Competencies"),
    path('allusers/<int:pk>/DeleteKPI', views.KPI_Delete.as_view(), name="Delete_User_KPI"),

    path('allusers/<int:pk>/UpdateG', views.Update_Goals_User.as_view(), name ="Update_User_Goals1"),
    path('allusers/<int:pk>/UpdateDepartmentalG', views.Update_Departmental_Goals.as_view(), name ='Update_Departmental_Goals'),
    path('allusers/<int:pk>/UpdateDepartmentalC', views.Update_Departmental_Competencies.as_view(), name='Update_Departmental_Competencies'),
    path('allusers/<int:pk>/UpdateC', views.Update_Competencies_User.as_view(), name='Update_User_Competencies'),
    path('allusers/<int:pk>/UpdateKPI', views.Update_KPI.as_view(), name ='Update_KPI'),
    path('allusers/<int:pk>/UpdateKPI_POST', views.Update_KPI_POST.as_view(), name ='Update_KPI_POST'),
    path('allusers/<int:pk>/UpdateKPI_POST1', views.Update_KPI_POST1.as_view(), name ='Update_KPI_POST1'),
    path('allusers/<int:pk>/UpdateKPI_POST2', views.Update_KPI_POST2.as_view(), name ='Update_KPI_POST2'),
    path('allusers/<int:pk>/UpdateDepartment', views.Update_Departments.as_view(), name='Update_Department'),

    path('allusers/<int:pk>/CreatetheGoals', views.createGoals, name='Create_User_Goals'),
    path('allusers/<int:pk>/<int:mk>/UpdateG', views.updateGoals, name ="Update_User_Goals"),

    path('allusers/<int:pk>/GoalsImage', views.GoalsImage, name='Goals_Image'),
    path('allusers/<int:pk>/UploadGoalsImage', views.GoalsImageUpload, name='Goals_ImageUpload'),
]

