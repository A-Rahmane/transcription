from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import TranscriptionJob
from .serializers import TranscriptionJobSerializer, TranscriptionSubmissionSerializer
from .tasks import run_transcription
from apps.media.models import File
from apps.media.permissions import HasFolderAccess

class TranscriptionJobViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    queryset = TranscriptionJob.objects.all()
    serializer_class = TranscriptionJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see jobs for files they have access to, or just their own jobs?
        # Spec says: "List user's jobs". So filter by file owner or job creator?
        # Job doesn't have an owner field directly, but file does.
        # Let's assume user wants to see jobs for files they own or have access to.
        # For simplicity and privacy, let's restrict to jobs where the user is the owner of the file.
        user = self.request.user
        return TranscriptionJob.objects.filter(file__owner=user)

    def create(self, request, *args, **kwargs):
        serializer = TranscriptionSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file_id = serializer.validated_data['file_id']
        file_obj = get_object_or_404(File, pk=file_id)
        
        # Check permission
        # User must be the owner of the file OR have explicit access to the folder.
        if file_obj.owner != request.user:
            has_access = False
            folder = file_obj.folder
            if folder:
                # Check if user is owner of the folder
                if folder.owner == request.user:
                    has_access = True
                else:
                    # Check recursive permissions (simplified for now: direct permission on this folder)
                    # Ideally we should use a service to check recursive permissions.
                    # For now, check if there is a Permission object for this user on this folder.
                    # We assume if they can view the folder, they can transcribe files in it.
                    from apps.media.models import Permission
                    has_access = Permission.objects.filter(
                        folder=folder, 
                        user=request.user, 
                        can_view=True
                    ).exists()
            
            if not has_access:
                return Response({"error": "You do not have permission to transcribe this file."}, status=status.HTTP_403_FORBIDDEN)

        # Create Job
        job = TranscriptionJob.objects.create(
            file=file_obj,
            language=serializer.validated_data.get('language')
        )
        
        # Trigger Celery Task
        run_transcription.delay(job.id)
        
        return Response(TranscriptionJobSerializer(job).data, status=status.HTTP_201_CREATED)
