# Transcription App Specification

## Overview
Handles the asynchronous transcription of audio/video files using local LLMs (Whisper). Manages the job queue to ensure efficient resource usage.

## Models
### `TranscriptionJob`
-   `file`: ForeignKey (File)
-   `status`: Enum (PENDING, PROCESSING, COMPLETED, FAILED)
-   `language`: String (Detected or User-specified)
-   `transcript_text`: TextField (JSON or Plain Text)
-   `created_at`: DateTime
-   `completed_at`: DateTime
-   `error_message`: TextField

## API Endpoints
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| POST | `/api/transcription/jobs/` | Submit a file for transcription | Permitted (File access) |
| GET | `/api/transcription/jobs/{id}/` | Get job status and result | Permitted |
| GET | `/api/transcription/jobs/` | List user's jobs | Authenticated |

## Key Logic
-   **Queue System**: Use **Celery** + **Redis** to manage the transcription queue.
-   **Local Inference**:
    -   Use `faster-whisper` or `whisper.cpp` for performance.
    -   Ensure only N jobs run concurrently (configurable, usually 1 or 2 depending on GPU).
-   **Result Storage**: Store the raw transcript (with timestamps) to allow for subtitle generation (.srt/.vtt) later.

## Implementation Roadmap
1.  **Celery Setup**: Configure Celery with Redis in Django.
2.  **Whisper Integration**: Create a Python service class to wrap the Whisper model.
3.  **Task Definition**: Write the Celery task that takes a `file_path` and runs Whisper.
4.  **API Implementation**: Endpoints to trigger the task and poll for status.
