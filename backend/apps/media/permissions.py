from rest_framework import permissions
from .models import Permission

class IsFolderOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Wait, actually we want to restrict read access too based on permissions.
        
        # This permission class specifically checks ownership.
        return obj.owner == request.user

class HasFolderAccess(permissions.BasePermission):
    """
    Checks if the user has access to the folder (or file's folder) recursively.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        # Determine the folder to check
        folder = None
        if hasattr(obj, 'folder'): # It's a File
            folder = obj.folder
        elif hasattr(obj, 'parent'): # It's a Folder
            folder = obj
        
        if folder is None:
            # Root folder or file without folder? 
            # If it's a root folder, check if user is owner.
            # If it's a file without folder (if allowed), check owner.
            if hasattr(obj, 'owner'):
                return obj.owner == user
            return False

        # Check ownership first
        if folder.owner == user:
            return True

        # Recursive check up the tree
        current_folder = folder
        while current_folder:
            # Check if permission exists for this folder
            try:
                perm = Permission.objects.get(folder=current_folder, user=user)
                if request.method in permissions.SAFE_METHODS:
                    if perm.can_view:
                        return True
                else:
                    # Write methods
                    if perm.can_edit:
                        return True
                    # Special case for upload? Handled in view logic usually, but here for general edit
            except Permission.DoesNotExist:
                pass
            
            current_folder = current_folder.parent
        
        return False
