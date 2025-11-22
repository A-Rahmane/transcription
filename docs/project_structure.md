# Project Structure Proposal

This structure separates the backend (Django) and frontend (React) into distinct directories for clarity and scalability.

```text
transcription-app/
├── backend/                # Django Project Root
│   ├── config/             # Project configuration (settings, urls)
│   ├── apps/               # Django Apps
│   │   ├── users/          # Authentication & User management
│   │   ├── media/          # Media upload/download & Folder management
│   │   ├── transcription/  # Whisper integration & Transcription logic
│   │   └── analysis/       # LLM summarization & Report generation
│   ├── media/              # User uploaded files (configured in settings)
│   ├── static/             # Static files (serving from Django)
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # React Application
│   ├── public/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components (routes)
│   │   ├── services/       # API calls (Axios/Fetch)
│   │   ├── context/        # Global state (Auth, Theme)
│   │   ├── hooks/          # Custom hooks
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── docs/                   # Project Documentation
│   ├── development/        # Backend & Frontend development specs and roadmaps
│   │   ├── users_spec.md
│   │   ├── media_spec.md
│   │   ├── analysis_spec.md
│   │   ├── transcription_spec.md
│   │   └── frontend_spec.md
│   ├── project_overview.md
│   ├── project_structure.md
│   ├── roadmap.md          # Only phase 1 roadmap : Project Initiation & Setup
│   └── recommendations.md
├── docker-compose.yml      # (Optional) For containerizing Backend, Frontend, MySQL
└── README.md
```

## Key Components

### Backend (Django)
-   **`apps/users`**: Handles registration, login (JWT recommended), and profile management.
-   **`apps/media`**: Models for `File`, `Folder`, and `Permission`. Handles file storage.
-   **`apps/transcription`**: Background workers to run Whisper inference without blocking the main thread.
-   **`apps/analysis`**: Integration with LLMs for summarization.

### Frontend (React)
-   **State Management**: Context API for managing auth state and file lists.
-   **UI Library**: Tailwind CSS for a polished look.
