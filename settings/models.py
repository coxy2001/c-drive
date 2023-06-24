from django.contrib.auth.models import User
from django.db import models

from pathlib import Path


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    base_path = models.CharField(max_length=128)

    def path(self):
        return Path(self.base_path).resolve()
