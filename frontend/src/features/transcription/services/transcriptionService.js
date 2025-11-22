import axios from '../../../utils/axios';

const startTranscription = async (fileId, language = 'en') => {
    try {
        const response = await axios.post('/transcription/jobs/', {
            file_id: fileId,
            language: language
        });
        return response.data;
    } catch (error) {
        console.error("Error starting transcription:", error);
        throw error;
    }
};

const getJobStatus = async (jobId) => {
    try {
        const response = await axios.get(`/transcription/jobs/${jobId}/`);
        return response.data;
    } catch (error) {
        console.error("Error fetching job status:", error);
        throw error;
    }
};

const getJobsByFile = async (fileId) => {
    try {
        // Currently the backend doesn't have a direct filter for jobs by file in the list endpoint
        // but we can filter on the client side or add a filter in the backend.
        const response = await axios.get('/transcription/jobs/');
        // Client-side filter for now as we didn't implement filter backend
        return response.data.filter(job => job.file === parseInt(fileId));
    } catch (error) {
        console.error("Error fetching jobs by file:", error);
        throw error;
    }
};

const transcriptionService = {
    startTranscription,
    getJobStatus,
    getJobsByFile
};

export default transcriptionService;
