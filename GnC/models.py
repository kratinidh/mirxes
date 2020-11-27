from django.db import models 
from datetime import datetime
from datetime import date
from Profile.models import Profile
from Profile.models import Departments
from Appraisals.models import Appraisal, Overall_Appraisal, User_Appraisal_List
from django.core.validators import MaxValueValidator, MinValueValidator
 
class goal_comment(models.Model):
    goal = models.ForeignKey('Goals', blank = False, null = False, on_delete = models.CASCADE)
    comments = models.CharField(max_length=3000, blank = False, null = True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, blank = False, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.created_by.name + ": " + self.comments

class competency_comment(models.Model):
    competency = models.ForeignKey('Competencies', blank = False, null = False, on_delete = models.CASCADE)
    comments = models.CharField(max_length=3000, blank = False, null = True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, blank = False, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.created_by.name + ": " + self.comments

class departmental_goal_comment(models.Model):
    departmental_goal = models.ForeignKey('Departmental_Goals', blank = False, null = False, on_delete = models.CASCADE)
    comments = models.CharField(max_length=3000, blank = False, null = True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, blank = False, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.created_by.name + ": " + self.comments

class departmental_competencies_comment(models.Model):
    departmental_competencies = models.ForeignKey('Departmental_Competencies', blank = False, null = False, on_delete = models.CASCADE)
    comments = models.CharField(max_length=3000, blank = False, null = True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, blank = False, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.created_by.name + ": " + self.comments

class KPI(models.Model):
    PROGRESS_CHOICES =(
        ('Working', 'Working'),
        ('Completed', 'Completed')
    )
    goal = models.ForeignKey('Goals', on_delete=models.CASCADE)
    description = models.CharField(max_length= 150)
    due = models.DateField(blank = True, null = True)
    date_created = models.DateField(null = True, default=date.today)
    progress = models.CharField(max_length = 20, blank = False, null = False, choices = PROGRESS_CHOICES, default = 'Working')

    def __str__(self):
        return self.description


class goal_category(models.Model):
    name = models.CharField (max_length = 70, blank=False, null = False)

    def __str__(self):
        return self.name

class Goals(models.Model):
    RATING_CHOICES = [
        (1, '1 - Major Improvement Needed'),
        (2, '2 - Needs Improvement'),
        (3, '3 - Meets Expectations'),
        (4, '4 - Exceeds Expectations'),
        (5, '5 - Far Exceed Expectations')
    ]
    
    TRACKING_CHOICES = [
        ('null', 'null'),
        ('On Track', 'On Track'),
        ('Not On Track', 'Not On Track')
    ]
    appraisal = models.ForeignKey(User_Appraisal_List, blank = False, null = True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(Profile, blank = False, null = True, on_delete=models.SET_NULL)
    summary = models.CharField(max_length=70, blank=False, null = False)
    goal_category = models.ForeignKey(goal_category, blank = False, null=True, on_delete = models.CASCADE)
    description = models.CharField(max_length=200, blank = True, null = True)
    due = models.DateField()
    weightage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank = False, null = False)
    metrics_Used = models.CharField(max_length = 100, blank=False, null=False, default='NIL')

    MID_user_comments = models.CharField(max_length = 2000, blank = False, null = False, default='NIL')
    MID_manager_comments=models.CharField(max_length= 2000, blank = False, null = False, default='NIL')
    
    user_rating = models.IntegerField(choices = RATING_CHOICES, blank = False, null = False, default = 1)
    manager_rating = models.IntegerField(choices = RATING_CHOICES, blank = False, null = False, default = 1)
    board_rating = models.IntegerField(choices = RATING_CHOICES, blank = False, null = False, default = 1)

    user_comments = models.CharField(max_length = 2000, blank = False, null = False, default='NIL')
    manager_comments=models.CharField(max_length= 2000, blank = False, null = False, default='NIL')
    board_comments=models.CharField(max_length= 2000, blank = False, null = False, default='NIL')
    tracking_status = models.CharField(max_length=50, blank = False, null = True, default = 'null', choices=TRACKING_CHOICES)
    metrics_evidence = models.ImageField(blank = True, null = True)

    def __str__(self):
        return self.summary

    def get_kpi_filtered_completed(self):
        return self.kpi_set.filter(progress='Completed')
    
    def get_kpi_percentage(self):
        total = self.kpi_set.all().count()
        cnt = self.kpi_set.filter(progress='Completed').count()
        if total <= 0:
            return -1
        elif total>=cnt:
            perc = int(cnt * 100 / total)
            return perc
        else:
            return 0

class competency_category(models.Model):
    name = models.CharField(max_length = 1000, blank = True, null = True)
    description = models.CharField(max_length = 1000, blank = False, null = False)

    def __str__(self):
        return "{} - {}".format(self.name, self.description)

class Competencies(models.Model):
    RATING_CHOICES = [
        (1, '1 - Major Improvement Needed'),
        (2, '2 - Needs Improvement'),
        (3, '3 - Meets Expectations'),
        (4, '4 - Exceeds Expectations'),
        (5, '5 - Far Exceed Expectations')
    ]

    appraisal = models.ForeignKey(User_Appraisal_List, blank = False, null = True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(Profile, blank = False, null = True, on_delete = models.SET_NULL)
    competency_category = models.ForeignKey(competency_category, blank = False, null = True, on_delete=models.CASCADE)
    summary = models.CharField(max_length = 150, blank = False, null = False)
    description = models.CharField(max_length=1000, blank= True, null = True)
    weightage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank = False, null = False)

    user_rating = models.IntegerField(choices = RATING_CHOICES, blank = False, null = False, default = 1)
    manager_rating = models.IntegerField(choices = RATING_CHOICES, blank = False, null = False, default = 1)
    board_rating = models.IntegerField(choices = RATING_CHOICES, blank = False, null = False, default = 1)

    user_comments = models.CharField(max_length = 2000, blank = False, null = False, default='NIL')
    manager_comments=models.CharField(max_length=2000, blank = False, null = False, default='NIL')
    board_comments=models.CharField(max_length= 2000, blank = False, null = False, default='NIL')

    def __str__(self):
        return self.summary

class Departmental_Goals(models.Model):
    manager = models.ForeignKey(Profile, blank = False, null = True, on_delete=models.SET_NULL)
    appraisal = models.ForeignKey(Overall_Appraisal, blank = False, null = True, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, null=True, on_delete=models.CASCADE)
    summary = models.CharField(max_length=70, blank=False, null = False)
    goal_category = models.ForeignKey(goal_category, blank = False, null = True, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank = True, null = True)
    due = models.DateField()

    def __str__(self):
        return self.summary

class Departmental_Competencies(models.Model):
    manager = models.ForeignKey(Profile, blank = False, null = True, on_delete=models.SET_NULL)
    appraisal = models.ForeignKey(Overall_Appraisal, blank = False, null = True, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, null=True, on_delete=models.CASCADE)
    summary = models.CharField(max_length=70, blank=False, null = False)
    competency_category = models.ForeignKey(goal_category, blank = False, null = True, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank = True, null = True)

    def __str__(self):
        return self.summary