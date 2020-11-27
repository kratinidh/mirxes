from django.db import models
from Profile.models import Profile
from datetime import date
from django.contrib.auth.models import Group, User, auth
from django.core.validators import MaxValueValidator, MinValueValidator
 
# Create your models here.

def GRADING_SYSTEM(x):
    if x>= 5:
        return 'Far Exceed Expectations'
    
    elif x>= 4:
        return 'Exceeds Expectations'

    elif x>= 3:
        return 'Meets Expectations'

    elif x>= 2:
        return 'Needs Improvement'

    elif x>= 1:
        return 'Major Improvement needed'

    else:
        return 'Ungraded'

def FINAL_GRADE(selfappraisal, overallappraisal):
    #Goals
    sum = 0
    weightage_count=0
    totalsum = 0
    for goal in selfappraisal.goals_set.all():
        weightage_count+=goal.weightage
    for goal in selfappraisal.goals_set.all():
        sum+=goal.user_rating * goal.weightage / weightage_count
    totalsum += sum * overallappraisal.goal_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for competency in selfappraisal.competencies_set.all():
        weightage_count+=competency.weightage
    for competency in selfappraisal.competencies_set.all():
        sum+=competency.user_rating * competency.weightage / weightage_count
    totalsum += sum * overallappraisal.competency_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for skill in selfappraisal.skills_set.all():
        weightage_count+=skill.weightage
    for skill in selfappraisal.skills_set.all():
        sum+=skill.user_rating * skill.weightage / weightage_count
    totalsum += sum * overallappraisal.skill_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    totalavg = round(totalsum,1)

    return totalavg
    #return GRADING_SYSTEM(totalavg)

def M_FINAL_GRADE(selfappraisal, overallappraisal):
    #Goals
    sum = 0
    weightage_count=0
    totalsum = 0
    for goal in selfappraisal.goals_set.all():
        weightage_count+=goal.weightage
    for goal in selfappraisal.goals_set.all():
        sum+=goal.manager_rating * goal.weightage / weightage_count
    totalsum += sum * overallappraisal.goal_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for competency in selfappraisal.competencies_set.all():
        weightage_count+=competency.weightage
    for competency in selfappraisal.competencies_set.all():
        sum+=competency.manager_rating * competency.weightage / weightage_count
    totalsum += sum * overallappraisal.competency_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for skill in selfappraisal.skills_set.all():
        weightage_count+=skill.weightage
    for skill in selfappraisal.skills_set.all():
        sum+=skill.manager_rating * skill.weightage / weightage_count
    totalsum += sum * overallappraisal.skill_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    totalavg = round(totalsum,1)

    return totalavg
    #return GRADING_SYSTEM(totalavg)

def B_FINAL_GRADE(selfappraisal, overallappraisal):
    #Goals
    sum = 0
    weightage_count=0
    totalsum = 0
    for goal in selfappraisal.goals_set.all():
        weightage_count+=goal.weightage
    for goal in selfappraisal.goals_set.all():
        sum+=goal.board_rating * goal.weightage / weightage_count
    totalsum += sum * overallappraisal.goal_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for competency in selfappraisal.competencies_set.all():
        weightage_count+=competency.weightage
    for competency in selfappraisal.competencies_set.all():
        sum+=competency.board_rating * competency.weightage / weightage_count
    totalsum += sum * overallappraisal.competency_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for skill in selfappraisal.skills_set.all():
        weightage_count+=skill.weightage
    for skill in selfappraisal.skills_set.all():
        sum+=skill.board_rating * skill.weightage / weightage_count
    totalsum += sum * overallappraisal.skill_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    totalavg = round(totalsum,1)

    return totalavg
   #return GRADING_SYSTEM(totalavg)

class Appraisal_Category(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
        
class Overall_Appraisal(models.Model):
    STAGES_CHOICES = (
        ('Stage 1', 'Goals Setting'),
        ('Stage 1B', 'Mid-Year Review'),
        ('Stage 2', 'Year-End Review'),
        ('Stage 3', 'Reports'),
        ('Stage 4', 'Calibration'),
        ('Completed', 'Completed')
    )

    RATING_CHOICES = (
        ('Denselight System', 'Denselight System'),
        ('MiRXes', 'MiRXes')
    )


    name = models.CharField(max_length = 50, blank = False, null = True)
    appraisal_category = models.ForeignKey(Appraisal_Category, null = True, blank = False, on_delete = models.SET_NULL)

    goal_weightage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank = False, null = True)
    competency_weightage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank = False, null = True)
    skill_weightage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank = False, null = True)

    start_date = models.DateField(default=date.today)
    goals_setting_end_date = models.DateField(default=date.today)

    mid_year_start_date = models.DateField(default=date.today)
    mid_year_end_date = models.DateField(default=date.today)
    
    end_year_start_date = models.DateField(default=date.today)
    appraisal_end_date = models.DateField(default=date.today)
    reports_end_date = models.DateField(default=date.today)
    calibration_end_date = models.DateField(default=date.today)

    #Temporary no foreignkey
    rating_scale = models.CharField(max_length= 50, blank = False, null = True, choices=RATING_CHOICES, default='Denselight System')
    
    status = models.CharField(max_length = 100, choices=STAGES_CHOICES, blank = False, null = True)

    def __str__(self):
        return '{}: {}'.format(self.appraisal_category, self.name)

class Rating_Scale(models.Model):
    name = models.CharField(max_length = 50, blank = False, null = False)
    description = models.CharField(max_length = 5000, blank = False, null = False)
    limiter = models.IntegerField(blank = False, null = False)

    def __str__(self):
        return self.name

class User_Appraisal_List(models.Model):
    RATING_CHOICES = [
        (1, '1 - Major Improvement Needed'),
        (2, '2 - Needs Improvement'),
        (3, '3 - Meets Expectations'),
        (4, '4 - Exceeds Expectations'),
        (5, '5 - Far Exceed Expectations')
    ]
    
    STATUS_CHOICE = (
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('S1BEmployee', 'S1BEmployee'),
        ('S1BManager', 'S1BManager'),
        ('S1BReview', 'S1BReview'),
        ('S2Employee', 'S2Employee'),
        ('S2Manager', 'S2Manager'),
        ('Approved', 'Approved')    
    )

    COMPLETION_CHOICE = (
        ('null', 'null'),
        ('ECompleted', 'ECompleted'),
        ('MCompleted', 'MCompleted'),
        ('BCompleted', 'BCompleted'),
        ('Review', 'Review'),
        ('ReviewCompleted', 'ReviewCompleted')
    )

    MID_YEAR_COMPLETION_CHOICE = (
        ('Uncompleted', 'Uncompleted'),
        ('Completed', 'Completed')
    )

    employee = models.ForeignKey(Profile, blank = False, null = True, on_delete=models.CASCADE)
    manager = models.ForeignKey(Profile, blank =False, null = True, related_name = "manager",on_delete=models.CASCADE)
    overall_appraisal = models.ForeignKey (Overall_Appraisal, blank = False, null = True, on_delete = models.CASCADE)

    status = models.CharField(max_length = 30, blank = False, null = False, choices=STATUS_CHOICE)
    appraisal_name = models.CharField(max_length = 50, blank = False, null = True)
    appraisal_category = models.ForeignKey(Appraisal_Category, blank = False, null = True, on_delete= models.SET_NULL)  
    
    overall_board_comments = models.CharField(max_length=5000, blank = True, null = True, default = 'No Comments')

    start_date = models.DateField(null = True)
    end_date = models.DateField(null = True)
    completion = models.CharField(max_length = 50, blank = False, null = True, default='null', choices = COMPLETION_CHOICE)

    goals_settingM_rejection = models.CharField(max_length = 3000, blank = False, null = False, default = 'NIL')
    mid_yearM_rejection = models.CharField(max_length = 3000, blank = False, null = False, default = 'NIL')
    appraisalHR_rejection = models.CharField(max_length = 3000, blank = False, null = False, default = 'NIL')
    mid_year_completion = models.CharField(max_length=15, choices=MID_YEAR_COMPLETION_CHOICE, blank = False, null = False, default = 'Uncompleted')

    incrementRecommendation = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank = False, null = False, default = 0)
    bonusRecommendation = models.CharField(max_length = 1000, blank = False, null = False, default = 'NIL')
    recommendationComments = models.CharField(max_length = 1000, blank = False, null = False, default = 'NIL')

    final_employee_rating = models.IntegerField(blank = True, null = True)
    final_manager_rating = models.IntegerField(blank = True, null = True)
    final_board_rating = models.IntegerField(blank = True, null = True)


    def __str__(self):
        return "{}:'s Appraisal".format(self.employee.name)

    def get_final_grade_user(self):    
        
        final_score = FINAL_GRADE(self, self.overall_appraisal)
        grades = GRADING_SYSTEM(final_score)
        return grades

    def get_final_grade_manager(self):    
        
        final_score = M_FINAL_GRADE(self, self.overall_appraisal)
        grades = GRADING_SYSTEM(final_score)
        return grades

    def get_final_grade_board(self):    
        
        final_score = B_FINAL_GRADE(self, self.overall_appraisal)
        grades = GRADING_SYSTEM(final_score)
        return grades

    def get_final_score_user(self):    
        
        final_score = FINAL_GRADE(self, self.overall_appraisal)
        return final_score

    def get_final_score_manager(self):    
        
        final_score = M_FINAL_GRADE(self, self.overall_appraisal)
        return final_score

    def get_final_score_board(self):    
        
        final_score = B_FINAL_GRADE(self, self.overall_appraisal)
        return final_score

    # def get_UAL_selfgoals(self):
    #     avg_weightage = 0
    #     weightage_check = 0
    #     goals = self.goals_set.all()
    #     for goal in goals:
    #         weightage_check += goal.weightage
        
    #     for goal in goals:
    #         avg_weightage += goal.user_rating * goal.weightage / weightage_check
        
    #     if weightage_check > 100:
    #         return -1
    #     else:
    #         return avg_weightage

    # def get_UAL_selfcompetencies(self):
    #     avg_weightage = 0
    #     weightage_check = 0
    #     competencies = self.competencies_set.all()
    #     for competency in competencies:
    #         weightage_check += competency.weightage
    #         avg_weightage += competency.user_rating * competency.weightage / weightage_check
        
    #     if weightage_check > 100:
    #         return -1
    #     else:
    #         return avg_weightage

    # def get_UAL_selfskills(self):
    #     avg_weightage = 0
    #     weightage_check = 0
    #     skills = self.skills_set.all()
    #     for skill in skills:
    #         weightage_check += skill.weightage
    #         avg_weightage += skill.user_rating * skill.weightage / weightage_check
        
    #     if weightage_check > 100:
    #         return -1
    #     else:
    #         return avg_weightage


    # def get_UAL_selfrating(self):
    #     sum = 0
    #     count = 0
    #     goals = self.goals_set.all()
    #     for goal in goals:
    #         sum += goal.user_rating
    #         count += 1
        
    #     competencies = self.competencies_set.all()
    #     for competency in competencies:
    #         sum += competency.user_rating
    #         count += 1
        
    #     skills = self.skills_set.all()
    #     for skill in skills:
    #         sum += skill.user_rating
    #         count+=1
        
    #     if count >= 1:
    #         return float(sum/count)
    #     else:
    #         return -1
    
    # def get_UAL_managerrating(self):
    #     sum = 0
    #     count = 0
    #     goals = self.goals_set.all()
    #     for goal in goals:
    #         sum += goal.manager_rating
    #         count += 1
        
    #     competencies = self.competencies_set.all()
    #     for competency in competencies:
    #         sum += competency.manager_rating
    #         count += 1
        
    #     skills = self.skills_set.all()
    #     for skill in skills:
    #         sum += skill.manager_rating
    #         count+=1
        
    #     return float(sum/count)
    
    # def get_UAL_boardrating(self):
    #     sum = 0
    #     count = 0
    #     goals = self.goals_set.all()
    #     for goal in goals:
    #         sum += goal.board_rating
    #         count += 1
        
    #     competencies = self.competencies_set.all()
    #     for competency in competencies:
    #         sum += competency.board_rating
    #         count += 1
        
    #     skills = self.skills_set.all()
    #     for skill in skills:
    #         sum += skill.board_rating
    #         count+=1
        
    #     return int(sum/count)


class Appraisal(models.Model):
    STATUS_CHOICE = (
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('HR', 'HR')
    )
    employee_list = models.OneToOneField(User_Appraisal_List, blank = False, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(Profile, blank=False, related_name="userA", null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(Profile, blank = False, related_name="managersA", null=True, on_delete=models.CASCADE)

    status = models.CharField(max_length = 30, blank = False, null = False, choices=STATUS_CHOICE)
    created_by = models.ForeignKey(Profile, blank = False, related_name="creatorA", null = True, on_delete=models.CASCADE)
    rating_scale = models.ForeignKey(Rating_Scale, null = True, blank = False, on_delete=models.SET_NULL)

    def __str__(self):
        return "{}'s Appraisal".format(self.employee_list)


class peerAppraisal(models.Model):
    COMPLETION_CHOICE = (
        ('Uncompleted', 'Uncompleted'),
        ('Completed', 'Completed')
    )
    appraisal = models.ForeignKey(User_Appraisal_List, blank = False, null = True, on_delete = models.CASCADE)
    manager = models.ForeignKey(Profile, blank = False, related_name="managersPA", null=True, on_delete=models.CASCADE)
    viewer = models.ForeignKey(Profile, blank = False, related_name="viewer", null=True, on_delete=models.CASCADE)

    title1 = models.CharField(max_length=200, blank = False, null = False)
    strength1 = models.CharField(max_length=3000, blank = True, null = True)
    weaknessdevelopment1 = models.CharField(max_length=3000, blank = True, null = True)

    title2 = models.CharField(max_length=200, blank = False, null = False, default = 'NIL')
    strength2 = models.CharField(max_length=3000, blank = True, null = True)
    weaknessdevelopment2 = models.CharField(max_length=3000, blank = True, null = True)

    title3 = models.CharField(max_length=200, blank = False, null = False, default = 'NIL')
    strength3 = models.CharField(max_length=3000, blank = True, null = True)
    weaknessdevelopment3 = models.CharField(max_length=3000, blank = True, null = True)


    completion = models.CharField(max_length=20, default = 'Uncompleted', blank = False, null = True, choices=COMPLETION_CHOICE)
    created_by = models.ForeignKey(Profile, blank = True, related_name="creatorPA", null = True, on_delete=models.CASCADE)

    
    def __str__(self):
        return "{}'s Peer Appraisal".format(self.appraisal)


class peerAppraisalQuestion(models.Model):
    COMPLETION_CHOICE = (
        ('Uncompleted', 'Uncompleted'),
        ('Completed', 'Completed')
    )

    appraisal = models.ForeignKey(peerAppraisal, blank = False, null = True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank = True, null = True)
    answer = models.CharField(max_length=1000, blank = True, null = True)
    completed = models.CharField(max_length=20, default = 'Uncompleted', blank = False, null = True, choices=COMPLETION_CHOICE)
