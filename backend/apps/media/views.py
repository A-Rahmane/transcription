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

    @action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='upload_chunk')
    def upload_chunk(self, request):
        serializer = ChunkedUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='complete_upload')
    def complete_upload(self, request):
        from django.db import transaction
        
        upload_id = request.data.get('upload_id')
        filename = request.data.get('filename')
        folder_id = request.data.get('folder_id')
        
        if not upload_id or not filename:
             return Response({'error': 'upload_id and filename are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate file extension
        allowed_extensions = ['.mp3', '.wav', '.mp4', '.m4a', '.mov', '.ogg', '.webm']
        import os
        ext = os.path.splitext(filename)[1].lower()
        if ext not in allowed_extensions:
            return Response({'error': f"Unsupported file extension. Allowed: {', '.join(allowed_extensions)}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Add select_for_update to prevent race conditions
                chunks = ChunkedUpload.objects.filter(upload_id=upload_id).select_for_update().order_by('offset')
                if not chunks.exists():
                    return Response({'error': 'No chunks found'}, status=status.HTTP_404_NOT_FOUND)

                # Check total size
                total_size = sum(chunk.file.size for chunk in chunks)
                limit_mb = 500
                if total_size > limit_mb * 1024 * 1024:
                     chunks.delete()
                     return Response({'error': f"Total file size exceeds limit of {limit_mb}MB."}, status=status.HTTP_400_BAD_REQUEST)

                import tempfile
                import shutil
                from django.core.files import File as DjangoFile

                tmp_path = None
                try:
                    # Assemble file to temporary path to avoid memory issues
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        for chunk in chunks:
                            with chunk.file.open('rb') as f:
                                shutil.copyfileobj(f, tmp_file, length=1024*1024) # 1MB chunks
                        tmp_path = tmp_file.name

                    # Create File object
                    folder = None
                    if folder_id:
                        folder = get_object_or_404(Folder, pk=folder_id)
                        if folder.owner != request.user:
                             perm = Permission.objects.filter(folder=folder, user=request.user, can_upload=True).exists()
                             if not perm:
                                 if tmp_path and os.path.exists(tmp_path):
                                    os.unlink(tmp_path)
                                 return Response({'error': 'No upload permission on this folder'}, status=status.HTTP_403_FORBIDDEN)

                    file_obj = File.objects.create(
                        name=filename,
                        folder=folder,
                        owner=request.user,
                        size=total_size
                    )
                    
                    # Save content to FileField
                    with open(tmp_path, 'rb') as f:
                        file_obj.file.save(filename, DjangoFile(f))
                    file_obj.save()

                    # Cleanup
                    os.unlink(tmp_path)
                    chunks.delete()

                    # Trigger async task
                    process_file_upload.delay(file_obj.id)

                    return Response(FileSerializer(file_obj).data, status=status.HTTP_201_CREATED)

                except Exception as e:
                    if tmp_path and os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                    raise e # Re-raise to trigger transaction rollback
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
