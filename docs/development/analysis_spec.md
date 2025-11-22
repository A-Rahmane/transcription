# Analysis App Specification

## Overview
Leverages LLMs to analyze transcribed text. Generates summaries, reports, translations, and extracts key points based on user prompts and system templates.

## Models
### `AnalysisRequest`
-   `transcription_job`: ForeignKey (TranscriptionJob)
-   `type`: Enum (SUMMARY, REPORT, TRANSLATION, CUSTOM)
-   `user_prompt`: TextField (Optional)
-   `system_prompt`: TextField (Used for the specific task)
-   `result_text`: TextField
-   `created_at`: DateTime

## API Endpoints
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| POST | `/api/analysis/generate/` | Request an analysis (summary, etc.) | Permitted |
| GET | `/api/analysis/requests/{id}/` | Get analysis result | Permitted |

## Key Logic
-   **LLM Integration**:
    -   Use a local LLM (e.g., Llama 3, Mistral) via `ollama` or `llama-cpp-python`.
    -   Alternatively, use an OpenAI-compatible API if a local server (like LM Studio) is running.
-   **Prompt Engineering**:
    -   Store standard system prompts for "Summarization", "Meeting Minutes", etc.
    -   Combine System Prompt + User Prompt + Transcript.
-   **Context Window**: Be mindful of the token limit. If the transcript is too long, implement a "Map-Reduce" or "Refine" strategy to summarize in chunks.

## Implementation Roadmap
1.  **LLM Service**: Create a service to interface with the local LLM provider.
2.  **Prompt Templates**: Define standard prompts for common tasks.
3.  **Analysis Task**: Create a Celery task for generation (LLMs can be slow).
4.  **API Implementation**: Endpoints to submit requests and view results.
