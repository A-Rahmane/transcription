from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from .models import Folder, File, Permission, ChunkedUpload
from .serializers import FolderSerializer, FolderDetailSerializer, FileSerializer, PermissionSerializer, ChunkedUploadSerializer
from .permissions import IsFolderOwner, HasFolderAccess
from .tasks import process_file_upload
import os

class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    permission_classes = [permissions.IsAuthenticated, HasFolderAccess]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FolderDetailSerializer
        return FolderSerializer

    def get_queryset(self):
        if self.action == 'list':
             user = self.request.user
             return Folder.objects.filter(parent__isnull=True, owner=user) | \
                    Folder.objects.filter(parent__isnull=True, permissions__user=user, permissions__can_view=True)
        return Folder.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsFolderOwner])
    def share(self, request, pk=None):
        folder = self.get_object()
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(folder=folder)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated, HasFolderAccess]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['post'], url_path='upload_chunk')
    def upload_chunk(self, request):
        serializer = ChunkedUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='complete_upload')
    def complete_upload(self, request):
        upload_id = request.data.get('upload_id')
        filename = request.data.get('filename')
        folder_id = request.data.get('folder_id')
        
        if not upload_id or not filename:
             return Response({'error': 'upload_id and filename are required'}, status=status.HTTP_400_BAD_REQUEST)

        chunks = ChunkedUpload.objects.filter(upload_id=upload_id).order_by('offset')
        if not chunks.exists():
            return Response({'error': 'No chunks found'}, status=status.HTTP_404_NOT_FOUND)

        # Assemble file
        file_content = b''
        for chunk in chunks:
            with chunk.file.open('rb') as f:
                file_content += f.read()
            # Clean up chunk
            chunk.delete() # Or keep for history? Usually delete to save space.

        # Create File object
        folder = None
        if folder_id:
            folder = get_object_or_404(Folder, pk=folder_id)
            # Check permission on folder?
            # HasFolderAccess should handle it if we were accessing a folder object, 
            # but here we are creating a file. 
            # We should check if user has upload permission on this folder.
            # For now, let's assume if they can see it they can upload (or check explicit permission)
            # Logic: Owner or can_upload=True
            if folder.owner != request.user:
                 perm = Permission.objects.filter(folder=folder, user=request.user, can_upload=True).exists()
                 if not perm:
                     return Response({'error': 'No upload permission on this folder'}, status=status.HTTP_403_FORBIDDEN)

        file_obj = File.objects.create(
            name=filename,
            folder=folder,
            owner=request.user,
            size=len(file_content)
        )
        file_obj.file.save(filename, ContentFile(file_content))
        file_obj.save()

        # Trigger async task
        process_file_upload.delay(file_obj.id)

        return Response(FileSerializer(file_obj).data, status=status.HTTP_201_CREATED)
