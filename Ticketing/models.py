from django.db import models
from Profile.models import Profile

class Ticket_Comments(models.Model):
    ticket= models.ForeignKey('Ticket', null = True, blank = False, on_delete=models.CASCADE)
    user= models.ForeignKey(Profile, null = False, blank = False, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank = False, null = False)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return 'Comment: {} by {}'.format(self.comment, self.user.name)


class Ticket(models.Model):
    CATEGORY_CHOICES=(
        ('Profile', 'PROFILE'),
        ('Employee Management', 'EMPLOYEE MANAGEMENT'),
        ('Goals and Competencies', 'GOALS AND COMPETENCIES'),
        ('Appraisals', 'APPRAISALS'),
        ('Trainings', 'TRAININGS'),
        ('Reports', 'REPORTS'),
        ('Ticketing', 'TICKETING'),
        ('Guide', 'GUIDE'),
        ('Careers', 'CAREERS'),
        ('Others', 'OTHERS')
    )

    STATUS_CHOICE=(
        ('Pending', 'PENDING'),
        ('Working', 'WORKING'),
        ('Awaiting Reply', 'AWAITING REPLY'),
        ('Solved', 'SOLVED')
    )
    category=models.CharField(max_length = 30, choices = CATEGORY_CHOICES, blank = False, null = False)

    title = models.CharField(max_length=50, blank = False, null = False)

    description = models.CharField(max_length = 5000, blank = True, null = True)

    status = models.CharField(max_length = 50, blank = False, null = False, default=STATUS_CHOICE[0][0])

    created_by= models.ForeignKey(Profile, blank = False, null = False, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
