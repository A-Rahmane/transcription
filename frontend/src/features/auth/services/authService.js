import axios from '../../../utils/axios';

const register = async (userData) => {
    const response = await axios.post('/auth/register/', userData);
    return response.data;
};

const login = async (username, password) => {
    const response = await axios.post('/auth/login/', { username, password });
    if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
    }
    return response.data;
};

const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
};

const getCurrentUser = async () => {
    const response = await axios.get('/users/me/');
    return response.data;
};

const authService = {
    register,
    login,
    logout,
    getCurrentUser,
};

export default authService;
