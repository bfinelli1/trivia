from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Group(models.Model):
    categoryid = models.PositiveSmallIntegerField(default=0)
    categoryname = models.CharField(max_length=256, default="")

    def __str__(self):
        return f"{self.categoryname}, {self.categoryid}"

    def serialize(self):
        return {
            "id": self.pk,
            "categoryname": self.categoryname
        }

class User(AbstractUser):
    profilepic = models.URLField(null=True)

    def __str__(self):
        return f"{self.username} score: {self.score}"


class Scores(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="quiz_group")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participant")
    numscore = models.PositiveIntegerField(default=0)
    numcompleted = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "groupid": self.group.pk,
            "user": self.user.username,
            "id": self.pk,
            "numscore": self.numscore,
            "numcompleted": self.numcompleted
    }