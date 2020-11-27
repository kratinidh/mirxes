from django.contrib import admin
from .models import Trainings, Apply_Trainings, Survey_Trainings, Skills, skill_category, Career_Discussion, Training_Courses
# Register your models here.

admin.site.register(Trainings)
admin.site.register(Apply_Trainings)
admin.site.register(Survey_Trainings)
admin.site.register(Skills)
admin.site.register(skill_category)
admin.site.register(Career_Discussion)
admin.site.register(Training_Courses)