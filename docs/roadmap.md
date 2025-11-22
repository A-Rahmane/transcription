# Phase 1 Roadmap: Project Initiation & Setup

This roadmap focuses on getting the foundational elements in place: setting up the environment, creating the basic project structure, and establishing the core database models.

## 1. Environment Setup
-   [x] Install Python & Django.
-   [x] Install Node.js & React (Vite).
-   [x] Install MySQL and create a database.
-   [x] Set up a virtual environment for the backend.

## 2. Backend Initialization (Django)
-   [x] Initialize Django project (`django-admin startproject`).
-   [x] Configure database settings (MySQL connection).
-   [x] Create Django Apps: `users`, `media`, `transcription`.
-   [ ] **User Authentication**:
    -   Implement Custom User Model (AbstractUser).
    -   Set up JWT authentication (SimpleJWT).
-   [ ] **Database Modeling**:
    -   Define `Folder` and `File` models.
    -   Define `Permission` model for sharing.

## 3. Frontend Initialization (React)
-   [x] Initialize React project (`npm create vite@latest`).
-   [ ] Install dependencies (Axios, React Router, UI Framework).
-   [ ] Set up basic routing (Login, Dashboard).
-   [ ] Create a basic Authentication context.
