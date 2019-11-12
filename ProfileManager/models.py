from django.db import models


# Create your models here.
class Users(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)


class Employee(models.Model):

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    type_choices = [
        ('0', 'Manager'),
        ('1', 'Employee'),
    ]
    company_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=gender_choices)
    hobbies = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=type_choices)
    profile_picture = models.ImageField(upload_to='profiles/')

    objects = models.Manager()