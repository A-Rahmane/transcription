import axios from '../../../utils/axios';

const requestAnalysis = async (jobId, type, prompt = '') => {
    try {
        const response = await axios.post('/analysis/requests/', {
            transcription_job_id: jobId,
            type: type,
            user_prompt: prompt
        });
        return response.data;
    } catch (error) {
        console.error("Error requesting analysis:", error);
        throw error;
    }
};

const getAnalyses = async (jobId) => {
    try {
        // Similar to transcription, we might need to filter.
        // The backend AnalysisRequestViewSet filters by `transcription_job__file__owner=user`.
        // It doesn't seem to support filtering by job ID directly in the URL params by default
        // unless we added it.
        // Let's client-side filter for now.
        const response = await axios.get('/analysis/requests/');
        return response.data.filter(req => req.transcription_job === parseInt(jobId));
    } catch (error) {
        console.error("Error fetching analyses:", error);
        throw error;
    }
};

const analysisService = {
    requestAnalysis,
    getAnalyses
};

export default analysisService;
