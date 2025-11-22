import React from 'react';
import { Link } from 'react-router-dom';

const FileItem = ({ file, onDelete }) => {
    return (
        <div className="flex items-center justify-between p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
            <Link to={`/media/files/${file.id}`} className="flex items-center space-x-3 truncate flex-grow hover:text-indigo-600">
                <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="text-gray-700 truncate font-medium">{file.name}</span>
            </Link>
            <div className="flex space-x-2">
                <button
                    onClick={() => onDelete(file.id)}
                    className="text-red-500 hover:text-red-700 p-1"
                >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
            </div>
        </div>
    );
};

const FileList = ({ files, onDelete }) => {
    if (!files || files.length === 0) {
        return <div className="text-gray-500 text-center py-8">No files in this folder.</div>;
    }

    return (
        <div className="space-y-2">
            {files.map((file) => (
                <FileItem key={file.id} file={file} onDelete={onDelete} />
            ))}
        </div>
    );
};

export default FileList;
