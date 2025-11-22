# Media App

## Purpose
Handles file uploads, folder organization, and permission management.

## Key Components
- **Models**: `Folder`, `File`, `Permission`, `ChunkedUpload`.
- **Permissions**: Recursive permission checking (`IsFolderOwner`, `HasFolderAccess`).
- **Views**: `FolderViewSet`, `FileViewSet` (supports chunked uploads).
