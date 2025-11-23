from rest_framework import serializers
from .models import Folder, File, Permission, ChunkedUpload
from django.contrib.auth import get_user_model

User = get_user_model()

class PermissionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Permission
        fields = ('id', 'folder', 'user', 'user_email', 'can_view', 'can_edit', 'can_upload')
        read_only_fields = ('id', 'folder')

class FileSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = File
        fields = ('id', 'name', 'file', 'folder', 'owner', 'owner_username', 'uploaded_at', 'size')
        read_only_fields = ('id', 'owner', 'uploaded_at', 'size')

    def validate_file(self, value):
        # Check file size (e.g., limit to 500MB)
        limit_mb = 500
        if value.size > limit_mb * 1024 * 1024:
            raise serializers.ValidationError(f"File size too large. Limit is {limit_mb}MB.")
        
        # Check file extension (allow audio/video)
        # Check file extension (allow audio/video)
        allowed_extensions = ['.mp3', '.wav', '.mp4', '.m4a', '.mov', '.ogg', '.webm']
        import os
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(f"Unsupported file extension. Allowed: {', '.join(allowed_extensions)}")
        
        return value

class FolderSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    # We might want to list subfolders and files here, or in a separate view.
    # For now, let's keep it simple.

    class Meta:
        model = Folder
        fields = ('id', 'name', 'parent', 'owner', 'owner_username', 'created_at')
        read_only_fields = ('id', 'owner', 'created_at')

    def validate_name(self, value):
        # Sanitize folder name
        from django.utils.html import escape
        value = escape(value.strip())
        if not value:
            raise serializers.ValidationError("Folder name cannot be empty")
        if len(value) > 255:
            raise serializers.ValidationError("Folder name too long")
        # Prevent path traversal
        if '/' in value or '\\' in value or '..' in value:
            raise serializers.ValidationError("Invalid folder name")
        return value

class FolderDetailSerializer(FolderSerializer):
    subfolders = FolderSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta(FolderSerializer.Meta):
        fields = FolderSerializer.Meta.fields + ('subfolders', 'files', 'permissions')

class ChunkedUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChunkedUpload
        fields = ('id', 'upload_id', 'file', 'offset', 'user', 'status', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
