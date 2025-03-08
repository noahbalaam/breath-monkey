from django.db import models
from django.contrib.auth.models import User 


class BreathingTechnique(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    name = models.CharField(max_length=255)
    in_time = models.IntegerField()
    in_hold_time = models.IntegerField(null=True, blank=True, default=0)
    out_time = models.IntegerField()
    out_hold_time = models.IntegerField(null=True, blank=True, default=0)
    is_global = models.BooleanField(default=False)  # Mark base techniques

    def __str__(self):
        return self.name

class BreathingPhase(models.Model):
    technique = models.ForeignKey(BreathingTechnique, on_delete=models.CASCADE, related_name="phases")
    name = models.CharField(max_length=50, choices=[
        ('Inhale', 'Inhale'),
        ('Hold', 'Hold'),
        ('Exhale', 'Exhale')
    ])
    duration = models.PositiveIntegerField(help_text="Duration in seconds")

    def __str__(self):
        return f"{self.technique.name} - {self.name} ({self.duration}s)"
    
class BreathingStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    technique = models.ForeignKey(BreathingTechnique, on_delete=models.SET_NULL, null=True, blank=True)
    session_duration = models.PositiveIntegerField(
        help_text="Session duration in seconds", 
        null=True, 
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.session_duration} seconds on {self.timestamp}"
