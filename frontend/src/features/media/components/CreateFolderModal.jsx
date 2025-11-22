import React, { useState } from 'react';

const CreateFolderModal = ({ isOpen, onClose, onCreate }) => {
    const [folderName, setFolderName] = useState('');

    if (!isOpen) return null;

    const handleSubmit = (e) => {
        e.preventDefault();
        onCreate(folderName);
        setFolderName('');
        onClose();
    };

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
            <div className="bg-white p-5 rounded-lg shadow-xl w-96">
                <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">Create New Folder</h3>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                        placeholder="Folder Name"
                        value={folderName}
                        onChange={(e) => setFolderName(e.target.value)}
                        autoFocus
                        required
                    />
                    <div className="mt-4 flex justify-end space-x-3">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 focus:outline-none"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none"
                        >
                            Create
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CreateFolderModal;
