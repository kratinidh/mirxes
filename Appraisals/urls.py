from django.urls import path

from . import views

app_name = 'Appraisals'
urlpatterns = [

    path('allusers/Create_AppraisalCategory', views.Create_Appraisal_Category.as_view(), name="Create_Appraisal_Category"),
    path('allusers/<int:pk>/Create_User_Appraisal_List', views.Create_User_Appraisal_List.as_view(), name="Create_User_Appraisal_List"),

    path('allusers/<int:pk>/UpdateOverallAppraisal',views.update_Overall_Appraisal, name="Update_Overall_Appraisal"),
    #path('allusers/<int:pk>/<int:mk>/Update', views.UpdateAppraisal, name="Update_Appraisal"),

    path('allusers/<int:pk>/OverallAppraisal', views.Detail_Overall_Appraisal.as_view(), name="Detail_Overall_Appraisal"),
    path('allusers/<int:pk>/<int:mk>/UserAppraisal/', views.Detail_User_Appraisal_List.as_view(), name="Detail_User_Appraisal"),
    path('allusers/<int:pk>/<int:mk>/HRUserAppraisal/', views.Detail_HRUser_Appraisal_List.as_view(), name="HRDetail_User_Appraisal"),

    path('allusers/<int:pk>/DeleteUserAppraisal', views.Delete_User_Appraisal_List.as_view(), name="Delete_User_Appraisal"),
    path('allusers/<int:pk>/DeleteOverallAppraisal', views.Delete_Overall_Appraisal.as_view(), name='Delete_Overall_Appraisal'),

    path('allusers/<int:pk>/EtM/AppraisalFlow', views.EtM_User_Appraisal_List.as_view(), name='EtM_Appraisal'),
    path('allusers/<int:pk>/MtE/AppraisalFlow', views.MtE_User_Appraisal_List.as_view(), name='MtE_Appraisal'),
    path('allusers/<int:pk>/MtS1BE', views.MtS1BE_User_Appraisal_List.as_view(), name='MtS1BE_Appraisal'),

    path('allusers/<int:pk>/S1BEtS1BM', views.S1BEtS1BM_User_Appraisal_List.as_view(), name='S1BEtS1BM_Appraisal'),
    path('allusers/<int:pk>/S1BMtS1BR', views.S1BMtS1BR_User_Appraisal_List.as_view(), name='S1BMtS1BR_Appraisal'),
    path('allusers/<int:pk>/S1BRtS1BM', views.S1BRtS1BM_User_Appraisal_List.as_view(), name='S1BRtS1BM_Appraisal'),
    path('allusers/<int:pk>/S1BMtS2E', views.S1BMtS2E_User_Appraisal_List.as_view(), name='S1BMtS2E_Appraisal'),

    path('allusers/<int:pk>/S2EtS2M', views.S2EtS2M_User_Appraisal_List.as_view(), name='S2EtS2M_Appraisal'),
    path('allusers/<int:pk>/S2MtApp', views.S2MtApp_User_Appraisal_List.as_view(), name='S2MtApp_Appraisal'),
    path('allusers/<int:pk>/ApptS2M', views.ApptS2M_User_Appraisal_List.as_view(), name='ApptS2M_Appraisal'),
    path('allusers/<int:pk>/S2MtAppR', views.S2MtAppR_User_Appraisal_List.as_view(), name='S2MtAppR_Appraisal'),
   # path('allusers/<int:pk>/<int:mk>/Update1', views.updateAppraisal2.as_view(), name="Update_Appraisal1")
    path('allusers/<int:pk>/UpdateMidYear/UpdateG/', views.UpdateMidAppraisalG, name="Update_MIDAppraisalG"),
    path('allM/<int:pk>/UpdateMidYear/UpdateG/', views.UpdateMidAppraisalG_M, name="Update_MIDAppraisalG_M"),

    path('allusers/<int:pk>/Update/UpdateS/UpdateC/UpdateG/', views.UpdateAppraisalG, name="Update_AppraisalG"),
    path('allusers/<int:pk>/Update/UpdateS/UpdateC/', views.UpdateAppraisalC, name='Update_AppraisalC'),
    path('allusers/<int:pk>/Update/UpdateS/', views.UpdateAppraisalS, name='Update_AppraisalS'),
    path('allusers/<int:pk>/Update/Career', views.createCareerDiscussion, name='Update_AppraisalCareer'),
    path('allusers/<int:pk>/Update/', views.Update_Appraisal, name='Update_Appraisal'),

    path('allM/<int:pk>/Update/UpdateS/UpdateC/UpdateG/', views.UpdateAppraisalG_M, name="Update_AppraisalG_M"),
    path('allM/<int:pk>/Update/UpdateS/UpdateC/', views.UpdateAppraisalC_M, name='Update_AppraisalC_M'),
    path('allM/<int:pk>/Update/UpdateS/', views.UpdateAppraisalS_M, name='Update_AppraisalS_M'),
    path('allM/<int:pk>/Update/Career', views.UpdateAppraisalCareer_M, name='Update_AppraisalCareer_M'),
    path('allM/<int:pk>/Update/', views.Update_Appraisal_M, name='Update_Appraisal_M'),

    path('allHR/<int:pk>/Update/UpdateS/UpdateC/UpdateG/', views.UpdateAppraisalG_B, name="Update_AppraisalG_B"),
    path('allHR/<int:pk>/Update/UpdateS/UpdateC/', views.UpdateAppraisalC_B, name='Update_AppraisalC_B'),
    path('allHR/<int:pk>/Update/UpdateS/', views.UpdateAppraisalS_B, name='Update_AppraisalS_B'),
    path('allHR/<int:pk>/Update/Career', views.UpdateAppraisalCareer_B, name='Update_AppraisalCareer_B'),
    path('allHR/<int:pk>/Update/', views.Update_Appraisal_B, name='Update_Appraisal_B'),


    #Checkbox User Appraisals
    path('allHR/<int:pk>/AddUserAppraisal_Indiv', views.Add_User_Appraisal_Indiv, name='Invite_Indiv_User_Appraisal'),
    path('allHR/<int:pk>/AddUserAppraisal_Dept', views.Add_User_Appraisal_Dept, name='Invite_Dept_User_Appraisal'),
    path('allHR/<int:pk>/AddUserAppraisal_Company', views.Add_User_Appraisal_Company, name='Invite_Company_User_Appraisal'),

    path('allusers/Create_Peer_Appraisal', views.Create_Peer_Appraisal, name="Create_Peer_Appraisal"),
    path('allusers/<int:pk>/Update_Peer_Appraisal', views.Update_Peer_Appraisal, name="Update_Peer_Appraisal"),
    
    # path('allusers/<int:pk>/Add_peerAppraisalQuestions', views.Add_peerAppraisalQn, name='Add_PeerAppraisalQn'),

    path('allusers/Create_OverallAppraisal/Stage1', views.create_Overall_Appraisal_Stage1, name="Create_Overall_Appraisal1"),
    path('allusers/<int:pk>/Create_OverallAppraisal/Stage3', views.create_Overall_Appraisal_Stage3, name="Create_Overall_Appraisal_Stage3"),
    path('allusers/<int:pk>/Create_OverallAppraisal/Stage4', views.create_Overall_Appraisal_Stage4, name="Create_Overall_Appraisal_Stage4"),

    path('allusers/<int:pk>/<int:mk>/<int:dk>/PersonalRecord/OverallAppraisal/Detail', views.PersonalAppraisalReport, name="Detail_PersonalRecord_OverallApp"),


    path('allusers/<int:pk>/CompanyRecord/OverallAppraisal/FAR', views.Comp_FinalAppReport, name='Comp_FAReport'),
    path('allusers/<int:pk>/CompanyRecord/ExportFAR', views.export_FinalAppraisalReport, name='export_FAReport'),

    path('allusers/<int:pk>/CompanyRecord/OverallAppraisal/FPR', views.Comp_FinalPayoutReport, name='Comp_FPReport'),
    path('allusers/<int:pk>/CompanyRecord/ExportFPR', views.export_FinalPayoutReport, name='export_FPReport'),

    path('allusers/<int:pk>/CompanyRecord/OverallAppraisal/IRR', views.Comp_IncremRecommReport, name='Comp_IRReport'),
    path('allusers/<int:pk>/CompanyRecord/ExportIRR', views.export_IncremRecommReport, name='export_IRReport'),

    path('allusers/<int:pk>/CompanyRecord/OverallAppraisal/TRR', views.Comp_TrainingRecommReport, name='Comp_TRReport'),
    path('allusers/<int:pk>/CompanyRecord/ExportTRR', views.export_TrainingRecommReport, name='export_TRReport'),

    path('allusers/<int:pk>/CompanyRecord/OverallAppraisal/CR', views.Comp_CalibrationReport, name='Comp_CPReport'),
]