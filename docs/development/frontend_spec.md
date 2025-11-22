# Frontend Specification & Roadmap

## Overview
The frontend is a Single Page Application (SPA) built with **React**, **Vite**, and **TypeScript**. It uses **Material UI (MUI)** for the design system to ensure a polished, professional look.

## Architecture
### Directory Structure
```text
src/
├── assets/         # Static assets (images, global css)
├── components/     # Reusable UI components
│   ├── common/     # Buttons, Inputs, Modals
│   ├── layout/     # Sidebar, Header, MainLayout
│   └── media/      # FileCard, FolderRow, UploadWidget
├── context/        # Global State (AuthContext, ThemeContext)
├── hooks/          # Custom Hooks (useAuth, useFileSystem)
├── pages/          # Page Components (Routes)
│   ├── auth/       # Login, Register
│   ├── dashboard/  # Main File Browser
│   └── detail/     # File Detail & Transcription View
├── services/       # API Integration (Axios instances)
├── types/          # TypeScript interfaces
└── utils/          # Helper functions (formatters, validators)
```

## Key Features & Components

### 1. Authentication
-   **AuthContext**: Manages JWT tokens (access/refresh), user profile state, and login/logout methods.
-   **Interceptors**: Axios interceptor to automatically attach the Bearer token and handle 401 Token Expired errors by refreshing the token.

### 2. Media Browser (Dashboard)
-   **Layout**: Sidebar (Navigation), Main Content Area.
-   **Folder Navigation**: Breadcrumbs for path navigation.
-   **File List**: Grid or List view of files and folders.
-   **Upload**: Drag-and-drop zone with progress bars for chunked uploads.

### 3. Transcription & Analysis View
-   **Transcript Viewer**: Read-only or editable text area showing the transcript.
-   **Action Panel**: Buttons to trigger "Summarize", "Translate", or "Generate Report".
-   **Result Display**: Markdown renderer for LLM-generated content.

## Implementation Roadmap

### Phase 1: Foundation & Auth
-   [ ] **Setup**: Configure Vite, TypeScript, ESLint, Prettier.
-   [ ] **Theme**: Set up MUI ThemeProvider with custom colors/typography.
-   [ ] **Routing**: Configure `react-router-dom` with protected routes.
-   [ ] **API Service**: Create Axios instance with interceptors.
-   [ ] **Auth**: Implement Login and Register pages + AuthContext.

### Phase 2: Media Management
-   [ ] **Layout**: Create the main Dashboard layout (Sidebar + Header).
-   [ ] **File Browser**: Implement Folder/File display components.
-   [ ] **Navigation**: Implement Breadcrumbs and Folder navigation logic.
-   [ ] **Upload**: Implement basic file upload (then upgrade to chunked).

### Phase 3: Transcription & Analysis
-   [ ] **Detail Page**: Create a page to view a single file.
-   [ ] **Transcription UI**: Display status (Pending/Processing) and final text.
-   [ ] **Analysis UI**: Interface to request summaries and view results.

### Phase 4: Polish & Advanced Features
-   [ ] **Sharing**: UI for managing folder permissions.
-   [ ] **Search**: Global search bar.
-   [ ] **Responsive Design**: Ensure mobile compatibility.
