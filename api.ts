import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
                    refresh_token: refreshToken,
                });

                const { access_token, refresh_token } = response.data;
                localStorage.setItem('access_token', access_token);
                localStorage.setItem('refresh_token', refresh_token);

                originalRequest.headers.Authorization = `Bearer ${access_token}`;
                return api(originalRequest);
            } catch (refreshError) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    register: (data: { email: string; password: string; full_name: string }) =>
        api.post('/auth/register', data),
    login: (email: string, password: string) =>
        api.post('/auth/login', new URLSearchParams({ username: email, password }), {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        }),
    refresh: (refreshToken: string) =>
        api.post('/auth/refresh', { refresh_token: refreshToken }),
};

// User API
export const userAPI = {
    getMe: () => api.get('/users/me'),
    updateMe: (data: any) => api.patch('/users/me', data),
    updatePresence: (status: string) => api.post('/users/presence', { status }),
    getUser: (userId: string) => api.get(`/users/${userId}`),
};

// Workspace API
export const workspaceAPI = {
    create: (data: any) => api.post('/workspaces', data),
    list: () => api.get('/workspaces'),
    get: (workspaceId: string) => api.get(`/workspaces/${workspaceId}`),
    invite: (workspaceId: string, email: string) =>
        api.post(`/workspaces/${workspaceId}/invite`, { email }),
};

// Channel API
export const channelAPI = {
    create: (data: any) => api.post('/channels', data),
    list: (workspaceId: string) => api.get(`/channels?workspace_id=${workspaceId}`),
    get: (channelId: string) => api.get(`/channels/${channelId}`),
    addMember: (channelId: string, userId: string) =>
        api.post(`/channels/${channelId}/members`, { user_id: userId }),
};

// Message API
export const messageAPI = {
    send: (workspaceId: string, data: any) =>
        api.post(`/messages?workspace_id=${workspaceId}`, data),
    list: (params: any) => api.get('/messages', { params }),
    addReaction: (messageId: string, emoji: string) =>
        api.post(`/messages/${messageId}/reactions`, { emoji }),
};

// File API
export const fileAPI = {
    upload: (file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        return api.post('/files/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    },
    download: (fileId: string) => api.get(`/files/${fileId}/download`),
};

// Search API
export const searchAPI = {
    messages: (query: string, workspaceId: string, channelId?: string) =>
        api.get('/search/messages', { params: { query, workspace_id: workspaceId, channel_id: channelId } }),
};

// Bot API
export const botAPI = {
    create: (data: any) => api.post('/bots', data),
    list: (workspaceId: string) => api.get(`/bots?workspace_id=${workspaceId}`),
    regenerateToken: (botId: string) => api.post(`/bots/${botId}/regenerate-token`),
};
