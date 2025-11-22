# Users App Specification

## Overview
Handles user authentication, registration, and profile management. Uses JWT (JSON Web Tokens) for secure, stateless authentication.

## Models
### `User` (Inherits from `AbstractUser`)
-   **Fields**: Standard Django User fields (username, email, password, pseudo).
-   **Extensions**: `pseudo` (Display name).

## API Endpoints
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| POST | `/api/auth/register/` | Register a new user | Public |
| POST | `/api/auth/login/` | Login and obtain JWT pair | Public |
| POST | `/api/auth/refresh/` | Refresh access token | Public |
| GET | `/api/users/me/` | Get current user profile | Authenticated |
| PATCH | `/api/users/me/` | Update profile (password, pseudo) | Authenticated |

## Implementation Roadmap
1.  **Setup JWT**: Configure `SimpleJWT` settings (lifetime, rotation).
2.  **Registration API**: Create serializer and view for user registration.
3.  **Profile API**: Create serializer and view for retrieving/updating user details.
4.  **Frontend Integration**: Implement Login/Register forms and AuthContext.

## Note: User Roles Clarification
**System Admin**
* Manages *users and system configuration*.
* Identified by `is_staff` / `is_superuser` flags in Django.
* Does **not** participate in the main workflow (no content operations on folders/files).

**Folder Roles (Managed in Media App)**
* **Owner**: Creator of a folder. Full control.
* **Editor**: Read/Write access to specific folders.
* **Viewer**: Read-only access to specific folders.
