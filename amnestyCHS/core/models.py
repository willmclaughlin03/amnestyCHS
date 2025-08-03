from django.db import models

class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"