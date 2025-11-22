import React, { useState, useEffect } from 'react';
import transcriptionService from '../services/transcriptionService';

const TranscriptionPanel = ({ fileId }) => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [language, setLanguage] = useState('en');

    const fetchJobs = async () => {
        try {
            const data = await transcriptionService.getJobsByFile(fileId);
            setJobs(data);
        } catch (err) {
            console.error("Failed to fetch jobs", err);
        }
    };

    useEffect(() => {
        fetchJobs();
        const interval = setInterval(fetchJobs, 5000); // Poll every 5s
        return () => clearInterval(interval);
    }, [fileId]);

    const handleStart = async () => {
        setLoading(true);
        try {
            await transcriptionService.startTranscription(fileId, language);
            fetchJobs();
        } catch (err) {
            console.error("Failed to start transcription", err);
            alert("Failed to start transcription");
        } finally {
            setLoading(false);
        }
    };

    const latestJob = jobs.length > 0 ? jobs[jobs.length - 1] : null;

    return (
        <div className="bg-white shadow rounded-lg p-6 mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Transcription</h3>

            {!latestJob && (
                <div className="flex items-center space-x-4">
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    >
                        <option value="en">English</option>
                        <option value="fr">French</option>
                        <option value="es">Spanish</option>
                    </select>
                    <button
                        onClick={handleStart}
                        disabled={loading}
                        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none"
                    >
                        {loading ? 'Starting...' : 'Start Transcription'}
                    </button>
                </div>
            )}

            {latestJob && (
                <div>
                    <div className="mb-4">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${latestJob.status === 'COMPLETED' ? 'bg-green-100 text-green-800' :
                                latestJob.status === 'FAILED' ? 'bg-red-100 text-red-800' :
                                    'bg-yellow-100 text-yellow-800'
                            }`}>
                            {latestJob.status}
                        </span>
                        <span className="ml-2 text-sm text-gray-500">
                            {new Date(latestJob.created_at).toLocaleString()}
                        </span>
                    </div>

                    {latestJob.status === 'COMPLETED' && (
                        <div className="mt-4">
                            <h4 className="text-sm font-medium text-gray-700 mb-2">Transcript:</h4>
                            <div className="bg-gray-50 p-4 rounded-md text-sm text-gray-800 whitespace-pre-wrap max-h-96 overflow-y-auto">
                                {latestJob.transcript_text}
                            </div>
                        </div>
                    )}

                    {latestJob.status === 'FAILED' && (
                        <div className="mt-2 text-sm text-red-600">
                            {latestJob.error_message}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default TranscriptionPanel;
