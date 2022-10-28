from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Group(models.Model):
    groupname = models.CharField(max_length=24)
    categoryid = models.PositiveSmallIntegerField(default=0)
    categoryname = models. CharField(max_length=256, default="")

    def __str__(self):
        return f"{self.groupname}"

    def serialize(self):
        return {
            "groupname": self.groupname,
            "id": self.pk,
            "categoryname": self.categoryname
        }

class User(AbstractUser):
    score = models.PositiveIntegerField(default=0)
    profilepic = models.URLField(null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name="participants")

    def __str__(self):
        return f"{self.username} score: {self.score}"


class Scores(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="quiz_group")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participant")
    numscore = models.PositiveIntegerField(default=0)
    numcompleted = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "groupname": self.group.groupname,
            "groupid": self.group.pk,
            "user": self.user.username,
            "id": self.pk,
            "numscore": self.numscore,
            "numcompleted": self.numcompleted
    }