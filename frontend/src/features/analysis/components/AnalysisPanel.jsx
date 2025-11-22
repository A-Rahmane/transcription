import React, { useState, useEffect } from 'react';
import analysisService from '../services/analysisService';
import transcriptionService from '../../transcription/services/transcriptionService';

const AnalysisPanel = ({ fileId }) => {
    const [analyses, setAnalyses] = useState([]);
    const [jobs, setJobs] = useState([]);
    const [selectedType, setSelectedType] = useState('SUMMARY');
    const [prompt, setPrompt] = useState('');
    const [loading, setLoading] = useState(false);

    const fetchData = async () => {
        try {
            const jobsData = await transcriptionService.getJobsByFile(fileId);
            setJobs(jobsData);

            const completedJob = jobsData.find(j => j.status === 'COMPLETED');
            if (completedJob) {
                const analysesData = await analysisService.getAnalyses(completedJob.id);
                setAnalyses(analysesData);
            }
        } catch (err) {
            console.error("Failed to fetch analysis data", err);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000);
        return () => clearInterval(interval);
    }, [fileId]);

    const completedJob = jobs.find(j => j.status === 'COMPLETED');

    const handleRequest = async (e) => {
        e.preventDefault();
        if (!completedJob) return;

        setLoading(true);
        try {
            await analysisService.requestAnalysis(completedJob.id, selectedType, prompt);
            fetchData();
            setPrompt('');
        } catch (err) {
            console.error("Failed to request analysis", err);
            alert("Failed to request analysis");
        } finally {
            setLoading(false);
        }
    };

    if (!completedJob) {
        return (
            <div className="bg-white shadow rounded-lg p-6 text-gray-500">
                Analysis available after transcription completes.
            </div>
        );
    }

    return (
        <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">AI Analysis</h3>

            <form onSubmit={handleRequest} className="mb-6 space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Type</label>
                    <select
                        value={selectedType}
                        onChange={(e) => setSelectedType(e.target.value)}
                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    >
                        <option value="SUMMARY">Summary</option>
                        <option value="REPORT">Report</option>
                        <option value="TRANSLATION">Translation</option>
                        <option value="CUSTOM">Custom</option>
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Prompt (Optional)</label>
                    <textarea
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        rows={3}
                        className="mt-1 block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border border-gray-300 rounded-md"
                        placeholder="Additional instructions..."
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none"
                >
                    {loading ? 'Generating...' : 'Generate Analysis'}
                </button>
            </form>

            <div className="space-y-4">
                {analyses.map((analysis) => (
                    <div key={analysis.id} className="border-t pt-4">
                        <div className="flex justify-between items-start mb-2">
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                {analysis.type}
                            </span>
                            <span className={`text-xs font-medium ${analysis.status === 'COMPLETED' ? 'text-green-600' :
                                    analysis.status === 'FAILED' ? 'text-red-600' : 'text-yellow-600'
                                }`}>
                                {analysis.status}
                            </span>
                        </div>
                        {analysis.status === 'COMPLETED' && (
                            <div className="bg-gray-50 p-3 rounded text-sm text-gray-800 whitespace-pre-wrap">
                                {analysis.result_text}
                            </div>
                        )}
                        {analysis.status === 'FAILED' && (
                            <div className="text-sm text-red-600">
                                {analysis.error_message}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AnalysisPanel;
