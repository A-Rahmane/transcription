from django.db import models
from apps.media.models import File

class TranscriptionJob(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='transcription_jobs')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    language = models.CharField(max_length=50, blank=True, null=True, help_text="Detected or specified language")
    transcript_text = models.TextField(blank=True, null=True, help_text="JSON or plain text transcript")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Job {self.id} for {self.file.name} ({self.status})"
