from django.contrib import admin
from .models import KPI, goal_category, Goals, competency_category,Competencies, Departmental_Goals, Departmental_Competencies, goal_comment, competency_comment
# Register your models here.
admin.site.register(KPI)
admin.site.register(goal_category)
admin.site.register(Goals)
admin.site.register(Departmental_Goals)
admin.site.register(Departmental_Competencies)
admin.site.register(competency_category)
admin.site.register(Competencies)
admin.site.register(goal_comment)
admin.site.register(competency_comment)
