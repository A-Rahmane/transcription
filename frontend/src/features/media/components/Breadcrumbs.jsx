import React from 'react';
import { Link } from 'react-router-dom';

const Breadcrumbs = ({ currentFolder, path = [] }) => {
    // Note: To implement full breadcrumbs, we'd need the full path from the backend 
    // or recursively fetch parents. 
    // For now, let's assume we just show "Home" -> "Current Folder".
    // If we want full path, the backend FolderDetailSerializer should probably return ancestors.
    // Let's stick to simple for now: Home > ... > Current

    return (
        <nav className="flex text-gray-500 text-sm mb-4" aria-label="Breadcrumb">
            <ol className="inline-flex items-center space-x-1 md:space-x-3">
                <li className="inline-flex items-center">
                    <Link to="/media" className="hover:text-gray-900">
                        Home
                    </Link>
                </li>
                {currentFolder && (
                    <li>
                        <div className="flex items-center">
                            <svg className="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                            </svg>
                            <span className="ml-1 text-gray-700 font-medium md:ml-2">
                                {currentFolder.name}
                            </span>
                        </div>
                    </li>
                )}
            </ol>
        </nav>
    );
};

export default Breadcrumbs;
