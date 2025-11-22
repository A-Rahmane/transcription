# Media App Specification

## Overview
Manages file uploads, folder organization, and permission handling. This is the core content management system of the application.

## Models
### `Folder`
-   `name`: String
-   `parent`: ForeignKey (Self, Nullable)
-   `owner`: ForeignKey (User)
-   `created_at`: DateTime

### `File`
-   `name`: String
-   `file`: FileField (Stored in local volume)
-   `folder`: ForeignKey (Folder, Nullable)
-   `owner`: ForeignKey (User)
-   `uploaded_at`: DateTime
-   `size`: Integer

### `Permission`
-   `folder`: ForeignKey (Folder)
-   `user`: ForeignKey (User)
-   `can_view`: Boolean
-   `can_edit`: Boolean
-   `can_upload`: Boolean

## API Endpoints
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| GET | `/api/media/folders/` | List root folders | Authenticated |
| POST | `/api/media/folders/` | Create a folder | Authenticated |
| GET | `/api/media/folders/{id}/` | Get folder contents (files & subfolders) | Permitted |
| POST | `/api/media/files/upload/` | Upload a file (Chunked support) | Permitted |
| DELETE | `/api/media/files/{id}/` | Delete a file | Owner/Editor |
| POST | `/api/media/folders/{id}/share/` | Grant permissions to a user | Owner |

## Key Logic
-   **Recursive Permissions**: When checking access for a subfolder or file, check if the user has permission on any parent folder up the tree.
-   **Chunked Uploads**: Implement a mechanism to handle large file uploads in chunks to avoid timeouts.
-   **Storage**: Files are stored in `MEDIA_ROOT`. Database only holds paths.

## Implementation Roadmap
1.  **Folder CRUD**: API to create, list, and delete folders.
2.  **File Upload**: Basic upload first, then chunked upload optimization.
3.  **Permission System**: Implement `IsPermitted` permission class in DRF.
4.  **Sharing API**: Endpoint to add entries to the `Permission` table.
