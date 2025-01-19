import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'https://django-server-production-6689.up.railway.app/api/', // Backend base URL

//    baseURL: 'http://localhost:8000/api', // Backend base URL
    headers: {
        'Content-Type': 'application/json',
    },
});

export default apiClient;