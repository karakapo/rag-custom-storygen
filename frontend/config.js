// Backend API Configuration
const API_BASE_URL = 'http://localhost:8000';

// API endpoints
const API_ENDPOINTS = {
    CREATE_STORY_RAG: `${API_BASE_URL}/story/create/2`,
    CREATE_STORY_FREE: `${API_BASE_URL}/story/create/1`,
    GET_STORY: (id) => `${API_BASE_URL}/story/${id}`,
    DELETE_STORY: (id) => `${API_BASE_URL}/story/${id}`,
    GET_ALL_STORIES: `${API_BASE_URL}/stories`
}; 