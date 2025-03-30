from django.db import models
from django.contrib.auth.models import AbstractUser


# dev_9
# Create your models here.
class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    gender = models.CharField(
        verbose_name="성별", max_length=1, choices=GenderChoices.choices
    )
    JOBS = (
        ("P", "교수/강사(Professor/Lecturer)"),
        ("S", "학생(Student)"),
        ("R", "연구원(Researcher)"),
        ("E", "기타(Etc.)"),
    )
    job = models.CharField(verbose_name="직업", max_length=1, choices=JOBS)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    # dev_23
    old_cart = models.CharField(max_length=200, blank=True, null=True)
