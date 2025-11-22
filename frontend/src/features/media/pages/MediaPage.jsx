import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import mediaService from '../services/mediaService';
import FolderList from '../components/FolderList';
import FileList from '../components/FileList';
import Breadcrumbs from '../components/Breadcrumbs';
import CreateFolderModal from '../components/CreateFolderModal';
import UploadModal from '../components/UploadModal';

const MediaPage = () => {
    const { folderId } = useParams();
    const [currentFolder, setCurrentFolder] = useState(null);
    const [folders, setFolders] = useState([]);
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isCreateFolderOpen, setIsCreateFolderOpen] = useState(false);
    const [isUploadOpen, setIsUploadOpen] = useState(false);

    const fetchData = async () => {
        setLoading(true);
        try {
            const data = await mediaService.getFolders(folderId);
            if (folderId) {
                setCurrentFolder(data); // If folderId, data is FolderDetail
                setFolders(data.subfolders || []);
                setFiles(data.files || []);
            } else {
                setCurrentFolder(null);
                setFolders(data.subfolders || data); // If root, data is list of folders
                setFiles(data.files || []);
            }
            setError(null);
        } catch (err) {
            console.error("Error fetching media:", err);
            setError("Failed to load media.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, [folderId]);

    const handleCreateFolder = async (name) => {
        try {
            await mediaService.createFolder(name, folderId);
            fetchData();
        } catch (err) {
            console.error("Failed to create folder:", err);
            alert("Failed to create folder");
        }
    };

    const handleUploadFile = async (file) => {
        try {
            await mediaService.uploadFile(file, folderId);
            fetchData();
        } catch (err) {
            console.error("Failed to upload file:", err);
            alert("Failed to upload file");
        }
    };

    const handleDeleteFile = async (fileId) => {
        if (window.confirm("Are you sure you want to delete this file?")) {
            try {
                await mediaService.deleteFile(fileId);
                fetchData();
            } catch (err) {
                console.error("Failed to delete file:", err);
                alert("Failed to delete file");
            }
        }
    };

    if (loading) return <div className="p-4">Loading...</div>;
    if (error) return <div className="p-4 text-red-500">{error}</div>;

    return (
        <div className="container mx-auto p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-800">Media Library</h1>
                <div className="space-x-3">
                    <button
                        onClick={() => setIsCreateFolderOpen(true)}
                        className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
                    >
                        New Folder
                    </button>
                    <button
                        onClick={() => setIsUploadOpen(true)}
                        className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                    >
                        Upload File
                    </button>
                </div>
            </div>

            <Breadcrumbs currentFolder={currentFolder} />

            <div className="mb-8">
                <h2 className="text-lg font-semibold text-gray-700 mb-4">Folders</h2>
                <FolderList folders={folders} />
            </div>

            <div>
                <h2 className="text-lg font-semibold text-gray-700 mb-4">Files</h2>
                <FileList files={files} onDelete={handleDeleteFile} />
            </div>

            <CreateFolderModal
                isOpen={isCreateFolderOpen}
                onClose={() => setIsCreateFolderOpen(false)}
                onCreate={handleCreateFolder}
            />

            <UploadModal
                isOpen={isUploadOpen}
                onClose={() => setIsUploadOpen(false)}
                onUpload={handleUploadFile}
            />
        </div>
    );
};

export default MediaPage;
