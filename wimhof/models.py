from django.db import models
from django.contrib.auth.models import User

class WimHofSession(models.Model):
    """Model to store WimHof breathing session configurations."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    is_global = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class BreathingRound(models.Model):
    """Individual round within a WimHof session."""
    session = models.ForeignKey(WimHofSession, related_name='rounds', on_delete=models.CASCADE)
    round_number = models.PositiveIntegerField()
    breath_count = models.PositiveIntegerField(help_text="Number of breaths in this round")
    
    class Meta:
        ordering = ['round_number']
    
    def __str__(self):
        return f"{self.session.name} - Round {self.round_number}: {self.breath_count} breaths"

class WimHofStats(models.Model):
    """Track statistics for completed WimHof sessions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(WimHofSession, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Store hold times for each round
    round_data = models.JSONField(default=dict, help_text="JSON data with round stats")
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"