from django.db import models
from main.models import UserStore
from blog import settings
# class PermFinal(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     nameperm = models.CharField(max_length=50)
#     allowappaction =models.BooleanField()

class VerificationUser(models.Model):
    userstore = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    user_email = models.EmailField()
    verification_code = models.IntegerField()