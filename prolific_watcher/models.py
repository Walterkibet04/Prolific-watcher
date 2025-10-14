from django.db import models

class SeenStudy(models.Model):
    study_id = models.CharField(max_length=128, unique=True)
    name = models.TextField(blank=True, null=True)
    reward = models.CharField(max_length=64, blank=True, null=True)
    estimated_time = models.CharField(max_length=32, blank=True, null=True)
    country_code = models.CharField(max_length=8, blank=True, null=True)
    detected_at = models.DateTimeField(auto_now_add=True)
    raw = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-detected_at"]

    def __str__(self):
        return f"{self.study_id} — {self.name}"
