from django.db import models
from django.contrib.auth.models import User
import json


class Dataset(models.Model):
    """
    Model to store metadata for uploaded datasets.
    Maintains only the last 5 uploaded datasets per user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets', null=True, blank=True)
    name = models.CharField(max_length=255)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    total_equipment = models.IntegerField()
    average_flowrate = models.FloatField()
    average_pressure = models.FloatField()
    average_temperature = models.FloatField()
    type_distribution = models.JSONField()
    
    class Meta:
        ordering = ['-upload_timestamp']
        indexes = [
            models.Index(fields=['user', '-upload_timestamp']),
        ]
    
    def __str__(self):
        username = self.user.username if self.user_id else 'unknown'
        return f"{username} - {self.name} - {self.upload_timestamp}"
    
    @classmethod
    def maintain_limit(cls, limit=5):
        """
        Maintain only the last 'limit' datasets globally.
        Delete older datasets when limit is exceeded.
        """
        count = cls.objects.count()
        if count > limit:
            # Get datasets to delete (oldest ones beyond the limit)
            datasets_to_delete = cls.objects.all()[limit:]
            for dataset in datasets_to_delete:
                dataset.delete()
    
    @classmethod
    def maintain_limit_per_user(cls, user, limit=5):
        """
        Maintain only the last 'limit' datasets per user.
        Delete older datasets when limit is exceeded.
        """
        count = cls.objects.filter(user=user).count()
        if count > limit:
            # Get datasets to delete for this user (oldest ones beyond the limit)
            datasets_to_delete = cls.objects.filter(user=user)[limit:]
            for dataset in datasets_to_delete:
                dataset.delete()