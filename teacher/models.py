from django.db import models

# Create your models here.
# teacher/models.py
from django.db import models
from users.models import CustomUser

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='teachers/', blank=True, null=True)

    def __str__(self):
        return self.user.username
