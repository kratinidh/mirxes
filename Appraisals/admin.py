from django.contrib import admin
from .models import Appraisal_Category, Overall_Appraisal, Rating_Scale, User_Appraisal_List, Appraisal, peerAppraisal, peerAppraisalQuestion
# Register your models here.

admin.site.register(Appraisal_Category)
admin.site.register(Overall_Appraisal)
admin.site.register(Rating_Scale)
admin.site.register(User_Appraisal_List)
admin.site.register(Appraisal)
admin.site.register(peerAppraisal)
admin.site.register(peerAppraisalQuestion)

