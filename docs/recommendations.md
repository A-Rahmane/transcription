# Recommendations & Best Practices

## 1. Handling Large Media Files
-   **Chunked Uploads**: For large video/audio files, standard HTTP uploads might time out. Implement chunked uploads on the frontend and backend.
-   **Async Processing**: **Never** process/transcribe files in the main request thread. Use **Celery** with RabbitMQ to handle transcription in the background.
-   **Storage**: Store actual files in a dedicated storage system (a dedicated local volume), not directly in the database. Store only the *path* in MySQL.

## 2. Local LLM Inference (Whisper)
-   **Hardware**: Whisper requires significant RAM and preferably a GPU. Ensure the host machine has NVIDIA drivers installed if using CUDA.
-   **Performance**:
    -   Use `faster-whisper` for better performance than the standard OpenAI implementation.
    -   Quantized models (int8) can save memory with minimal accuracy loss.
-   **Queueing**: Since local inference is resource-intensive, implement a strict queue system so you don't crash the server by trying to transcribe 10 files at once.

## 3. Security & Permissions
-   **Trusted Environment**: Since the app is deployed on a local network for trusted employees, strict defense-in-depth against malicious authenticated users is lower priority. Focus on usability and accidental data loss prevention rather than advanced attack mitigation.
-   **Folder Access**: When implementing folder sharing, check permissions recursively. If a user has access to a parent folder, they inherit access to children.
-   **Input Validation**: Basic sanitization is still recommended to prevent accidental errors or simple injection issues, even with trusted users.

## 4. Frontend Experience
-   **Progress Bars**: Uploading and transcribing take time. Show real-time progress to the user (WebSocket or Polling).
-   **Optimistic UI**: When moving files or creating folders, update the UI immediately while the backend processes the request.
