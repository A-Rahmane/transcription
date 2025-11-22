# Transcription & Media Management App

## Overview
This project is a comprehensive web application for managing media files, performing audio/video transcription using local LLMs (Whisper), and generating AI-driven analysis (summaries, reports) using the Gemini API. It features a secure, folder-based organization system with granular permissions.

## Architecture
The project is divided into two main components:
- **Backend**: Django REST Framework application handling API requests, authentication, database interactions, and asynchronous tasks (Celery/Redis).
- **Frontend**: React application (Vite) providing a responsive user interface for media management and interaction.

## Key Features
- **User Authentication**: JWT-based auth with custom user profiles.
- **Media Management**: Upload, organize, and share files/folders with recursive permissions.
- **Transcription**: Asynchronous transcription of audio/video files using `faster-whisper`.
- **Analysis**: AI-powered summarization and reporting using Google Gemini.

## Getting Started
Please refer to the `backend/README.md` and `frontend/README.md` for specific setup instructions.
