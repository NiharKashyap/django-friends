from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Friends(models.Model):
    request_to = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    request_from = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('request_to', 'request_from')