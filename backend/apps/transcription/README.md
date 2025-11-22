# Transcription App

## Purpose
Manages transcription jobs and integrates with the Whisper model.

## Key Components
- **Models**: `TranscriptionJob`.
- **Services**: `WhisperService` (wraps `faster-whisper`).
- **Tasks**: `run_transcription` (Celery task).
- **Views**: `TranscriptionJobViewSet`.
