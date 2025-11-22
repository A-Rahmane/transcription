import React from 'react';
import { Link } from 'react-router-dom';

const FolderItem = ({ folder }) => {
    return (
        <Link to={`/media/${folder.id}`} className="block p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
            <div className="flex items-center space-x-3">
                <svg className="w-8 h-8 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" />
                </svg>
                <span className="text-gray-700 font-medium truncate">{folder.name}</span>
            </div>
        </Link>
    );
};

const FolderList = ({ folders }) => {
    if (!folders || folders.length === 0) {
        return null;
    }

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
            {folders.map((folder) => (
                <FolderItem key={folder.id} folder={folder} />
            ))}
        </div>
    );
};

export default FolderList;
