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

<<<<<<< HEAD
    career = models.CharField(max_length=200, default="")
=======
    career = models.CharField(max_length=100, default="")
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487

    uploaded_at = models.DateTimeField(auto_now_add=True)

    found_skills = models.TextField(default="")

    missing_skills = models.TextField(default="")

    recommendations = models.TextField(default="")

    improvements = models.TextField(default="")

<<<<<<< HEAD
    email = models.CharField(max_length=100, default="", blank=True)

    phone = models.CharField(max_length=50, default="", blank=True)

    education = models.TextField(default="", blank=True)

    experience = models.TextField(default="", blank=True)

    projects = models.TextField(default="", blank=True)

    certifications = models.TextField(default="", blank=True)

    interview_questions = models.TextField(default="", blank=True)

    ai_feedback = models.TextField(default="", blank=True)

=======
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
    def __str__(self):

        return self.name