from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import AnalysisRequest
from .serializers import AnalysisRequestSerializer, AnalysisSubmissionSerializer
from .tasks import run_analysis
from apps.transcription.models import TranscriptionJob

class AnalysisRequestViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    queryset = AnalysisRequest.objects.all()
    serializer_class = AnalysisRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter by user's access to the underlying transcription/file
        user = self.request.user
        return AnalysisRequest.objects.filter(transcription_job__file__owner=user)

    def create(self, request, *args, **kwargs):
        serializer = AnalysisSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        job_id = serializer.validated_data['transcription_job_id']
        job = get_object_or_404(TranscriptionJob, pk=job_id)
        
        # Check permission
        # Check permission using HasFolderAccess on the underlying file
        from apps.media.permissions import HasFolderAccess
        permission = HasFolderAccess()
        if not permission.has_object_permission(request, self, job.file):
             return Response({"error": "You do not have permission to analyze this job."}, status=status.HTTP_403_FORBIDDEN)

        # Determine System Prompt based on Type
        req_type = serializer.validated_data['type']
        system_prompt = "You are a helpful AI assistant."
        if req_type == AnalysisRequest.Type.SUMMARY:
            system_prompt = "You are an expert summarizer. Provide a concise summary of the following transcript."
        elif req_type == AnalysisRequest.Type.REPORT:
            system_prompt = "You are a professional analyst. Create a detailed report based on the following transcript, highlighting key points and action items."
        elif req_type == AnalysisRequest.Type.TRANSLATION:
            system_prompt = "You are a professional translator. Translate the following transcript."
        # Custom type uses default or user provided prompt implicitly via user_prompt

        # Create Request
        analysis_req = AnalysisRequest.objects.create(
            transcription_job=job,
            type=req_type,
            user_prompt=serializer.validated_data.get('user_prompt', ''),
            system_prompt=system_prompt
        )
        
        # Trigger Celery Task
        run_analysis.delay(analysis_req.id)
        
        return Response(AnalysisRequestSerializer(analysis_req).data, status=status.HTTP_201_CREATED)
