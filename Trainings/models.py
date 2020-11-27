from django.db import models
from Profile.models import discard_Skills, Profile
from Appraisals.models import User_Appraisal_List, Overall_Appraisal
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

#Currently useless
class Trainings(models.Model):
    name = models.CharField(max_length = 150, blank = False, null = False)
    skill_category = models.ForeignKey('skill_category', blank = False, null = True, on_delete=models.SET_NULL)
    provider = models.CharField(max_length = 150, blank = True, null = True)
    cost = models.FloatField(max_length = 150, blank = True, null = True)
    ratings = models.FloatField(max_length = 10, blank = True, null = True)

    def __str__(self):
        return self.name

class Training_Courses(models.Model):
    name = models.CharField(max_length = 150, blank = False, null = False)
    skill_category = models.ForeignKey('skill_category', blank = False, null = True, on_delete=models.SET_NULL)
    provider = models.CharField(max_length = 150, blank = True, null = True)
    cost = models.FloatField(max_length = 150, blank = True, null = True)
    ratings = models.FloatField(max_length = 10, blank = True, null = True)

    def __str__(self):
        return self.name

class Apply_Trainings(models.Model):
    STATUS_CHOICE = (
        ('Rejected', 'REJECTED'),
        ('Pending', 'PENDING'),
        ('Approved', 'APPROVED'),
        ('Completed', 'COMPLETED')
    )
    employee = models.ForeignKey(Profile, blank = False, null = True, on_delete = models.SET_NULL)
    training = models.ForeignKey(Trainings, blank = False, null = True, on_delete = models.SET_NULL)
    status = models.CharField(max_length=50, blank = False, null = False, choices=STATUS_CHOICE)
    date_start = models.DateField(blank = True, null = True)
    date_end = models.DateField(blank = True, null = True)
    approved_by = models.CharField(max_length=200, blank = True, null = True)

    def __class__(self):
        return self.employee + ":" + self.training

class Survey_Trainings(models.Model):
    RATING_CHOICE=(
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
        )
    training = models.ForeignKey(Trainings, null = True, on_delete=models.SET_NULL)
    objectives_met = models.IntegerField(blank = False, null = False, choices=RATING_CHOICE)
    content_design = models.IntegerField(blank = False, null = False, choices=RATING_CHOICE)
    trainer_knowledge = models.IntegerField(blank = False, null = False, choices=RATING_CHOICE)
    training_relevance = models.IntegerField(blank = False, null = False, choices=RATING_CHOICE)
    recommend_training = models.IntegerField(blank = False, null = False, choices=RATING_CHOICE)

    def __str__(self):
        return self.training

class Skills(models.Model):
    RATING_CHOICES = [
        (1, '1 - Major Improvement Needed'),
        (2, '2 - Needs Improvement'),
        (3, '3 - Meets Expectations'),
        (4, '4 - Exceeds Expectations'),
        (5, '5 - Far Exceed Expectations')
    ]
    
    appraisal = models.ForeignKey(User_Appraisal_List, blank = False, null = True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(Profile, blank = False, null = True, on_delete=models.SET_NULL)
    skill_category = models.ForeignKey('skill_category', blank = False, null=True, on_delete = models.CASCADE)
    description = models.CharField(max_length=1000, blank = True, null = True)
    weightage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank = False, null = False)

    recommended_Trainings_user = models.CharField(max_length=1000, blank = False, null = False, default ='NIL')
    recommended_Trainings_manager = models.CharField(max_length=1000, blank = False, null = False, default ='NIL')
    recommended_Trainings_board = models.CharField(max_length=1000, blank = False, null = False, default ='NIL')

    user_rating = models.IntegerField(choices = RATING_CHOICES, blank = False, null = False, default = 1)
    manager_rating = models.IntegerField(choices = RATING_CHOICES, blank = False, null = False, default = 1)
    board_rating = models.IntegerField(choices = RATING_CHOICES, blank = False, null = False, default = 1)

    user_comments = models.CharField(max_length = 2000, blank = False, null = False, default='NIL')
    manager_comments=models.CharField(max_length=2000, blank = False, null = False, default='NIL')
    board_comments=models.CharField(max_length= 2000, blank = False, null = False, default='NIL')

    def __str__(self):
        return self.description

class skill_category(models.Model):
    name = models.CharField(max_length=50, blank = False, null = False)

    def __str__(self):
        return self.name

class Career_Discussion(models.Model):
    employee = models.ForeignKey(Profile, blank = False, null = False, on_delete=models.CASCADE)
    user_appraisal = models.ForeignKey(User_Appraisal_List, null = False, blank = False,on_delete=models.CASCADE)

    Q1 = models.CharField(max_length=5000, blank = False, null = False, default = 'NIL')
    Q2 = models.CharField(max_length=5000, blank = False, null = False, default = 'NIL')
    Q3 = models.CharField(max_length=5000, blank = False, null = False, default = 'NIL')
    Q4 = models.CharField(max_length=5000, blank = False, null = False, default = 'NIL')
    Q5 = models.CharField(max_length=5000, blank = False, null = False, default = 'NIL')
    
    Q6 = models.CharField(max_length=5000, blank = False, null = False, default = 'NIL')
    Q7 = models.CharField(max_length=5000, blank = False, null = False, default = 'NIL')
    Q8 = models.CharField(max_length=5000, blank = False, null = False, default = 'NIL')

    
