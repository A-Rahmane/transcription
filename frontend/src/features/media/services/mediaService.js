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
    const data = { name };
    if (parentId) {
        data.parent = parentId;
    }
    const response = await axios.post('/media/folders/', data);
    return response.data;
};

const uploadFile = async (file, folderId = null) => {
    // Using the simple upload endpoint for now as per previous steps
    // /api/media/files/upload/ or /api/media/files/
    // The viewset has an 'upload' action at /media/files/upload/

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
};

const deleteFile = async (fileId) => {
    await axios.delete(`/media/files/${fileId}/`);
};

const deleteFolder = async (folderId) => {
    await axios.delete(`/media/folders/${folderId}/`);
};

const mediaService = {
    getFolders,
    createFolder,
    uploadFile,
    deleteFile,
    deleteFolder,
};

export default mediaService;
