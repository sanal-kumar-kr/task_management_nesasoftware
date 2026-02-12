from django.db import models
from django.conf import settings
import uuid
class Task(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completion_report = models.TextField(null=True, blank=True)
    worked_hours = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

from django.conf import settings

