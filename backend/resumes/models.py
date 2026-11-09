from django.conf import settings
from django.db import models

class CV(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cvs")
    title = models.CharField(max_length=160, default="My CV")
    language = models.CharField(max_length=2, choices=[("en", "English"), ("de", "Deutsch")], default="en")
    template = models.CharField(max_length=20, choices=[("modern", "Modern"), ("classic", "Classic")], default="modern")
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-updated_at"]
    def __str__(self):
        return f"{self.title} ({self.owner})"
