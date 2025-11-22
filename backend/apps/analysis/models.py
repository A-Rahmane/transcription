from django.db import models
from apps.transcription.models import TranscriptionJob

class AnalysisRequest(models.Model):
    class Type(models.TextChoices):
        SUMMARY = 'SUMMARY', 'Summary'
        REPORT = 'REPORT', 'Report'
        TRANSLATION = 'TRANSLATION', 'Translation'
        CUSTOM = 'CUSTOM', 'Custom'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    transcription_job = models.ForeignKey(TranscriptionJob, on_delete=models.CASCADE, related_name='analysis_requests')
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.SUMMARY)
    user_prompt = models.TextField(blank=True, null=True, help_text="Optional user instructions")
    system_prompt = models.TextField(blank=True, null=True, help_text="System prompt used for generation")
    result_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type} for Job {self.transcription_job.id} ({self.status})"
