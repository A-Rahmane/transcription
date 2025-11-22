# Backend - Transcription App

## Overview
The backend is built with Django and Django REST Framework. It manages the core logic, database (MySQL), and asynchronous processing (Celery + Redis).

## Apps
- **users**: User authentication and profile management.
- **media**: File and folder management with granular permissions.
- **transcription**: Transcription job management and Whisper integration.
- **analysis**: LLM-based analysis of transcripts.

## Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Database**: Ensure MySQL is running and configured in `config/settings.py`.
3. **Migrations**:
   ```bash
   python manage.py migrate
   ```
4. **Celery**:
   ```bash
   celery -A config worker -l info
   ```
5. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## Environment Variables
- `GEMINI_API_KEY`: Required for analysis features.
- `MYSQL_...`: Database credentials.
