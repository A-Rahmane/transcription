# Analysis App

## Purpose
Provides AI-powered analysis of transcripts using Large Language Models (LLMs).

## Key Components
- **Models**: `AnalysisRequest`.
- **Services**: `LLMService` (integrates with Gemini API).
- **Tasks**: `run_analysis` (Celery task).
- **Views**: `AnalysisRequestViewSet`.
