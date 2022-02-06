from django.db import models
from auth_api.models import UserProfile
from django.utils.timezone import now


# Create your models here.

class Company(models.Model):
    title = models.CharField(max_length=32, unique=True)
    employee = models.ManyToManyField(UserProfile, related_name='employee')
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Todo(models.Model):
    title = models.CharField(max_length=20, blank=True, unique_for_date='date')
    description = models.TextField(max_length=500, blank=True)
    date = models.DateTimeField(blank=True,default=now())
    in_progress = models.BooleanField(default=False,blank=True)
    is_done = models.BooleanField(default=False,blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True,blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Notes(models.Model):
    title = models.CharField(max_length=20, blank=False)
    description = models.TextField(max_length=300, blank=False)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
