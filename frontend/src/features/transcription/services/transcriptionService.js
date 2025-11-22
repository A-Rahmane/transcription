import axios from '../../../utils/axios';

const startTranscription = async (fileId, language = 'en') => {
    const response = await axios.post('/transcription/jobs/', {
        file_id: fileId,
        language: language
    });
    return response.data;
};

const getJobStatus = async (jobId) => {
    const response = await axios.get(`/transcription/jobs/${jobId}/`);
    return response.data;
};

const getJobsByFile = async (fileId) => {
    // Currently the backend doesn't have a direct filter for jobs by file in the list endpoint
    // but we can filter on the client side or add a filter in the backend.
    // For now, let's assume we might need to fetch all and filter, or better, 
    // let's rely on the FileDetailsPage to fetch the file which might include job info 
    // if we updated the serializer, OR we just list all jobs and filter.
    // Actually, the best way is to use the list endpoint with a query param if supported.
    // The backend TranscriptionJobViewSet uses standard ModelViewSet.
    // Let's assume we can filter by file if we added DjangoFilterBackend, 
    // but we didn't explicitly add it.
    // Alternative: The FileDetailSerializer could return the transcription jobs.
    // Let's check if we can just list all for now or if we need to update backend.
    // For simplicity in this step, let's assume we fetch the file details and it might have the job ID,
    // or we just create a new job.
    // Wait, the requirement says "manage transcription jobs".
    // Let's implement a simple list for now.
    const response = await axios.get('/transcription/jobs/');
    // Client-side filter for now as we didn't implement filter backend
    return response.data.filter(job => job.file === parseInt(fileId));
};

const transcriptionService = {
    startTranscription,
    getJobStatus,
    getJobsByFile
};

export default transcriptionService;
