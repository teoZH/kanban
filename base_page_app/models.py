from django.db import models
from accounts.models import UserProfile


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
    title = models.CharField(max_length=20, blank=False, unique_for_date='date')
    description = models.TextField(max_length=500, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    in_progress = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)

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
