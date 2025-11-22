import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from '../../../utils/axios';
import TranscriptionPanel from '../../transcription/components/TranscriptionPanel';
import AnalysisPanel from '../../analysis/components/AnalysisPanel';

const FileDetailsPage = () => {
    const { fileId } = useParams();
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchFile = async () => {
            try {
                // Assuming we can get file details from this endpoint.
                // If not, we might need to fetch from folder details or list.
                // The backend FileViewSet supports retrieve.
                const response = await axios.get(`/media/files/${fileId}/`);
                setFile(response.data);
            } catch (err) {
                console.error("Failed to fetch file", err);
                setError("Failed to load file details.");
            } finally {
                setLoading(false);
            }
        };
        fetchFile();
    }, [fileId]);

    if (loading) return <div className="p-6">Loading...</div>;
    if (error) return <div className="p-6 text-red-500">{error}</div>;
    if (!file) return <div className="p-6">File not found.</div>;

    return (
        <div className="container mx-auto p-6">
            <div className="mb-6">
                <Link to={`/media/${file.folder || ''}`} className="text-indigo-600 hover:text-indigo-800 mb-2 inline-block">
                    &larr; Back to Folder
                </Link>
                <h1 className="text-2xl font-bold text-gray-900">{file.name}</h1>
                <p className="text-gray-500 text-sm">Size: {(file.size / 1024).toFixed(2)} KB</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                    <TranscriptionPanel fileId={file.id} />
                </div>
                <div>
                    <AnalysisPanel fileId={file.id} />
                </div>
            </div>
        </div>
    );
};

export default FileDetailsPage;
