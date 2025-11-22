# Frontend - Transcription App

## Overview
The frontend is a React application built with Vite and Tailwind CSS. It provides the user interface for authentication, media management, and transcription/analysis interaction.

## Features
- **Auth**: Login and Registration with JWT support.
- **Media**: Folder browser, file upload, and management.
- **Transcription**: Interface to start jobs and view results.
- **Analysis**: Interface to request AI summaries and reports.

## Setup
1. **Install Dependencies**:
   ```bash
   npm install
   ```
2. **Development Server**:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

## Configuration
- **Proxy**: Configured in `vite.config.js` to forward `/api` requests to the backend (`http://localhost:8000`).
