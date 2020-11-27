from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator

class Qualifications(models.Model):
    employee = models.ForeignKey('Profile', blank = False, null = True, on_delete=models.CASCADE)
    institution = models.CharField(max_length = 150, blank = True, null = True)
    name = models.CharField(max_length = 150, blank=False, null = False)
    graduation_year = models.IntegerField(validators=[MinValueValidator(1920), MaxValueValidator(2200)],blank = True, null = True)

    def __str__(self):
        return self.name

class discard_Skills(models.Model):
    name = models.CharField(max_length = 150, blank = False, null = False)
    course_Attended = models.CharField(max_length = 150, blank = True, null = True)

    def __str__(self):
        return self.name

class Departments(models.Model):
    name = models.CharField(max_length=100, blank = False, null = True)

    manager = models.ForeignKey('Profile', blank = True, null = True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Profile(models.Model):
    EMPLOYMENT_TYPE_CHOICE = (
        ('Contractor', 'CONTRACTOR'),
        ('Full-time', 'FULL-TIME'),
        ('Part-time', 'PART-TIME'),
        ('Internship', 'INTERN'))

    GENDER_CHOICE = (
        ('Male', 'MALE'),
        ('Female', 'FEMALE')
    )

    MARITAL_STATUS_CHOICE =(
        ('Single', 'SINGLE'),
        ('Married', 'MARRIED'),
        ('Divorced', 'DIVORCED'),
        ('Separated', 'SEPARATED'),        
        ('Widowed', 'WIDOWED')
    )

    DIRECT_CHOICES = (
        ('DIRECT', 'DIRECT'),
        ('INDIRECT', 'INDIRECT')
    )

    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)

    profile_Picture = models.ImageField(blank = True, null = True)
    name = models.CharField(max_length = 200, blank = False, null = False)

    employee_ID = models.CharField(max_length=15, blank = False, null = False, default = 'S123456D')

    nric = models.CharField(max_length=20, blank = False, null = True)

    typeOfEmployee = models.CharField(max_length=50, blank = False, null = False, choices=DIRECT_CHOICES, default='DIRECT')

    email = models.EmailField(blank = False, null = False)

    department = models.ForeignKey(Departments, blank = False, null = True, on_delete=models.SET_NULL)

    gender = models.CharField(max_length = 6, choices=GENDER_CHOICE, blank = False, null = False)

    address_1 = models.CharField(("address"), max_length=250)
    address_2 = models.CharField(("address2"), max_length=250, blank=True)

    date_Of_Passport_Expiry = models.DateField(blank = True, null = True)

    citizenship_Status = models.CharField(max_length =100, blank=False, null=False, default = '-')

    date_Of_Hire = models.DateField(blank = False, null = False)

    job_Title = models.CharField(max_length = 100, blank = False, null = False)

    employment_Type=models.CharField(max_length = 30, choices= EMPLOYMENT_TYPE_CHOICE, default = 'Full-time')

    skill1 = models.CharField(max_length = 50, blank = True, null = True)
    skill2 = models.CharField(max_length = 50, blank = True, null = True)
    skill3 = models.CharField(max_length = 50, blank = True, null = True)


    first_Reporting_Manager = models.ForeignKey('self', blank = True, null = True, on_delete=models.SET_NULL)

    second_Reporting_Manager = models.CharField(max_length = 200, blank = True, null = True)

    division_Centre = models.CharField(max_length = 150, blank = True, null = True)

    phone = PhoneNumberField(blank = True, null = True)

    def __str__(self):
        return self.name



















