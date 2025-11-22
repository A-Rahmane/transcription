from rest_framework import serializers
from .models import TranscriptionJob
from apps.media.serializers import FileSerializer

class TranscriptionJobSerializer(serializers.ModelSerializer):
    file_details = FileSerializer(source='file', read_only=True)

    class Meta:
        model = TranscriptionJob
        fields = ('id', 'file', 'file_details', 'status', 'language', 'transcript_text', 'created_at', 'completed_at', 'error_message')
        read_only_fields = ('id', 'status', 'language', 'transcript_text', 'created_at', 'completed_at', 'error_message')

class TranscriptionSubmissionSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    language = serializers.CharField(required=False, allow_null=True)
