from celery import shared_task
from django.utils import timezone
from .models import TranscriptionJob
from .services import WhisperService
import json
import traceback

@shared_task
def run_transcription(job_id):
    try:
        job = TranscriptionJob.objects.get(id=job_id)
    except TranscriptionJob.DoesNotExist:
        return f"Job {job_id} not found."

    job.status = TranscriptionJob.Status.PROCESSING
    job.save()

    try:
        # Initialize service
        # TODO: Make model size configurable via settings or job parameters
        service = WhisperService(model_size="base") 
        
        # Get file path
        file_path = job.file.file.path
        
        # Run transcription
        result = service.transcribe(file_path)
        
        # Update job
        job.status = TranscriptionJob.Status.COMPLETED
        job.language = result.get('language')
        job.transcript_text = result.get('text', '') # Store plain text
        job.completed_at = timezone.now()
        job.save()
        
        return f"Job {job_id} completed successfully."

    except Exception as e:
        job.status = TranscriptionJob.Status.FAILED
        job.error_message = str(e) + "\n" + traceback.format_exc()
        job.save()
        return f"Job {job_id} failed: {str(e)}"
