# timesheet/models.py
from django.db import models
from django.conf import settings

class TimePunch(models.Model):
    PUNCH_TYPE_CHOICES = [
        ("IN", "Clock In"),
        ("OUT", "Clock Out"),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    punch_type = models.CharField(max_length=3, choices=PUNCH_TYPE_CHOICES)

    # ADD THIS NEW FIELD
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        # ... (no changes here) ...
        return f"{self.employee.username} - {self.get_punch_type_display()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"