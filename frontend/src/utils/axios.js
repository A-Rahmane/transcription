import axios from 'axios';

const instance = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

instance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

instance.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                try {
                    const response = await axios.post('/api/auth/refresh/', {
                        refresh: refreshToken,
                    });
                    if (response.status === 200) {
                        localStorage.setItem('access_token', response.data.access);
                        instance.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
                        return instance(originalRequest);
                    }
                } catch (refreshError) {
                    console.error("Token refresh failed:", refreshError);
                    // Logout user or redirect to login
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    window.location.href = '/login';
                }
            } else {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default instance;
