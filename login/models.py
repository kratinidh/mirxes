from django.db import models

class Login(models.Model):
    username = models.CharField(max_length = 100, blank = False, unique = True, null = False)
    password = models.CharField(max_length = 100, blank = False, null = False)

