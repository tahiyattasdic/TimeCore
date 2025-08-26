from django.db import models
from django.conf import settings

#managing clocking-in or clocking-out 
class TimePunch(models.Model):
    PUNCH_TYPE_CHOICES = [ #specifies the record
        ("IN", "Clock In"),
        ("OUT", "Clock Out"),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #links time punch to a specific employee
    timestamp = models.DateTimeField(auto_now_add=True) #records the date and time when the punch is created
    punch_type = models.CharField(max_length=3, choices=PUNCH_TYPE_CHOICES) #forces to choose fromt the two choices from the placeholder

    confirmed = models.BooleanField(default=False)

    def __str__(self):
        # ... (no changes here) ...
        return f"{self.employee.username} - {self.get_punch_type_display()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
#This is for the message icon in the dashboard to chat with the manager
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'From {self.sender.username} to {self.recipient.username} at {self.timestamp}'

    class Meta:
        ordering = ('timestamp',)