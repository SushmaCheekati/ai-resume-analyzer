from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    resume_file = models.FileField(upload_to='resumes/')

    score = models.IntegerField(default=0)

    career = models.CharField(max_length=100, default="")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    found_skills = models.TextField(default="")

    missing_skills = models.TextField(default="")

    recommendations = models.TextField(default="")

    improvements = models.TextField(default="")

    def __str__(self):

        return self.name