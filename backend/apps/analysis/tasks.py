from celery import shared_task
from django.utils import timezone
from .models import AnalysisRequest
from .services import LLMService
import traceback

@shared_task
def run_analysis(request_id):
    try:
        analysis_request = AnalysisRequest.objects.get(id=request_id)
    except AnalysisRequest.DoesNotExist:
        return f"AnalysisRequest {request_id} not found."

    analysis_request.status = AnalysisRequest.Status.PROCESSING
    analysis_request.save()

    try:
        # Initialize service
        service = LLMService()
        
        # Construct prompt
        transcript = analysis_request.transcription_job.transcript_text
        # If transcript is JSON, we might need to parse it to get just the text.
        # For now, let's assume it's the raw text or we pass it as is.
        # Ideally, we should extract the plain text from the JSON structure if it's stored as JSON.
        import json
        try:
            transcript_data = json.loads(transcript)
            if isinstance(transcript_data, dict) and 'text' in transcript_data:
                transcript_text = transcript_data['text']
            else:
                transcript_text = transcript
        except json.JSONDecodeError:
            transcript_text = transcript

        user_prompt = analysis_request.user_prompt or ""
        system_prompt = analysis_request.system_prompt or "You are a helpful assistant."
        
        # Combine prompts
        # Strategy: System Prompt + Context (Transcript) + User Instruction
        full_prompt = f"Transcript:\n{transcript_text}\n\nInstruction: {user_prompt}"
        
        # Run generation
        result = service.generate(full_prompt, system_prompt=system_prompt)
        
        # Update request
        analysis_request.status = AnalysisRequest.Status.COMPLETED
        analysis_request.result_text = result
        analysis_request.completed_at = timezone.now()
        analysis_request.save()
        
        return f"AnalysisRequest {request_id} completed successfully."

    except Exception as e:
        analysis_request.status = AnalysisRequest.Status.FAILED
        analysis_request.error_message = str(e) + "\n" + traceback.format_exc()
        analysis_request.save()
        return f"AnalysisRequest {request_id} failed: {str(e)}"
