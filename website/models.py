from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
	data = models.CharField(max_length=100, default='Nothing posted yet', blank=True, null=True)

	def __str__(self):
		return self.user.username
