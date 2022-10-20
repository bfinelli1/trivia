from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    score = models.PositiveIntegerField(default=0)
    profilepic = models.URLField(null=True)

    def __str__(self):
        return f"{self.username} ${self.score}"

class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    groupname = models.CharField(max_length=24)

    def __str__(self):
        return f"{self.groupname}"