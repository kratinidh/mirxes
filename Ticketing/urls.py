from . import views
from django.urls import path

app_name = 'Ticketing'
urlpatterns=[
    path('employee/', views.User_Ticketing, name ='User_Ticket'),
    path('HRd/', views.HR_Ticketing, name ='HR_Ticket'),

    path('allusers/CreateTicket', views.Create_Ticketing.as_view(), name='Create_User_Ticket'),
    path('allusers/CreateComments', views.Create_Comments.as_view(), name='Create_User_Comment'),

    path('allusers/<int:pk>', views.Detail_Ticket.as_view(), name='Detail_Ticket'),
    path('allusers/<int:pk>/DeleteT', views.Delete_Ticket.as_view(),name='Delete_Ticket'),
    path('allusers/<int:pk>/DeleteC', views.Delete_Comments.as_view(), name='Delete_Comment'),

    path('allusers/<int:pk>/UpdateT', views.Update_Ticketing.as_view(), name='Update_Ticket'),
    path('allusers/<int:pk>/UpdateC', views.Update_Comments.as_view(), name='Update_Comment')
]