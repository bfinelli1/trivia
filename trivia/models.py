from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Group(models.Model):
    groupname = models.CharField(max_length=24)
    num_participants = models.PositiveSmallIntegerField(default=0)
    maxparticipants = models.PositiveSmallIntegerField(default=8)
    qendtime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.groupname}"

    def serialize(self):
        return {
            "groupname": self.groupname,
            "num_participants": self.num_participants
        }

class User(AbstractUser):
    score = models.PositiveIntegerField(default=0)
    profilepic = models.URLField(null=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, related_name="participant")

    def __str__(self):
        return f"{self.username} score: {self.score}"


class Quiz(models.Model):
    num_questions = models.PositiveSmallIntegerField(default=0)
    pass

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    pass