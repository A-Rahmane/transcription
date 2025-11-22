# Project Overview: Transcription & Media Management App

## Goal
Create a web application that allows users to upload/download media, transcribe/translate audio/video using local LLMs (Whisper), and generate reports/summaries from the transcribed text. The app will also support folder organization and sharing with granular permissions.

## Core Features
1.  **Authentication**: Secure user registration and login.
2.  **Media Management**: Upload and download audio/video files.
3.  **Transcription & Translation**:
    -   Use local LLMs (e.g., OpenAI Whisper) for transcription.
    -   Support translation.
4.  **Content Generation**:
    -   Generate summaries, reports, and main points from transcripts.
    -   Allow users to mix their prompts with system prompts.
    -   Copy/download generated text.
5.  **Organization**:
    -   Folder-based structure for content.
6.  **Collaboration**:
    -   Share folders with other users.
    -   Granular permissions (view, edit, etc.) for invited users.

## Technology Stack
-   **Backend**: Django (Python)
-   **Frontend**: React (TypeScript)
-   **Database**: MySQL (Relational DBMS)
-   **AI/ML**: Local inference (Whisper) for transcription; potentially other LLMs for summarization (e.g., Llama, Mistral) and API integration if local resources are limited.

## Deployment Context
-   **Environment**: Local Intranet (Offline/Local Network with internet access).
-   **User Base**: Trusted employees within the company.
-   **Security Posture**: The system runs in a controlled internal environment with authenticated, trusted company users. Security focuses on internal access control and data handling rather than external threats.
