from rest_framework import serializers
from .models import AnalysisRequest

class AnalysisRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisRequest
        fields = '__all__'
        read_only_fields = ('id', 'result_text', 'status', 'created_at', 'completed_at', 'error_message')

class AnalysisSubmissionSerializer(serializers.Serializer):
    transcription_job_id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=AnalysisRequest.Type.choices, default=AnalysisRequest.Type.SUMMARY)
    user_prompt = serializers.CharField(required=False, allow_blank=True)
