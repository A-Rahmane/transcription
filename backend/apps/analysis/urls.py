from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalysisRequestViewSet

router = DefaultRouter()
router.register(r'requests', AnalysisRequestViewSet, basename='analysis-request')

urlpatterns = [
    path('', include(router.urls)),
    path('generate/', AnalysisRequestViewSet.as_view({'post': 'create'}), name='analysis-generate'), # Alias for create if needed
]
