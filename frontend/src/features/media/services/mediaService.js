import axios from '../../../utils/axios';

const getFolders = async (parentId = null) => {
    const params = parentId ? { parent: parentId } : {};
    // The backend list endpoint returns root folders if no filter is applied, 
    // or we might need to filter by parent.
    // Based on views.py: 
    // if self.action == 'list': return Folder.objects.filter(parent__isnull=True, ...)
    // So default list returns root folders.
    // To get subfolders, we might need to use the detail view of the parent folder 
    // which returns 'subfolders' in the serializer.

    if (parentId) {
        // Get folder details which includes subfolders and files
        const response = await axios.get(`/media/folders/${parentId}/`);
        return response.data;
    } else {
        // Get root folders
        const response = await axios.get('/media/folders/');
        return { subfolders: response.data, files: [] }; // Standardize structure
    }
};

const createFolder = async (name, parentId = null) => {
    try {
        const data = { name };
        if (parentId) {
            data.parent = parentId;
        }
        const response = await axios.post('/media/folders/', data);
        return response.data;
    } catch (error) {
        console.error("Error creating folder:", error);
        throw error;
    }
};

const uploadFile = async (file, folderId = null) => {
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('name', file.name);
        if (folderId) {
            formData.append('folder', folderId);
        }

        const response = await axios.post('/media/files/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error("Error uploading file:", error);
        throw error;
    }
};

const deleteFile = async (fileId) => {
    try {
        await axios.delete(`/media/files/${fileId}/`);
    } catch (error) {
        console.error("Error deleting file:", error);
        throw error;
    }
};

const deleteFolder = async (folderId) => {
    try {
        await axios.delete(`/media/folders/${folderId}/`);
    } catch (error) {
        console.error("Error deleting folder:", error);
        throw error;
    }
};

const mediaService = {
    getFolders,
    createFolder,
    uploadFile,
    deleteFile,
    deleteFolder,
};

export default mediaService;
