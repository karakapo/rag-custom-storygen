// This file (auth.js) has been cleared as all authentication functionality (register, login, logout)
// has been removed from the application based on user request.

// Initialize Supabase client
// IMPORTANT: Replace with your actual Supabase URL and Anon Key
// const SUPABASE_URL = 'YOUR_SUPABASE_URL';
// const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';

// const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Register new user function (removed)

// Event listener for the registration form (removed)

// API endpoint'leri
const API_BASE_URL = 'http://localhost:8000';

// Auth durumu değişikliğini bildir
function dispatchAuthStateChanged() {
    window.dispatchEvent(new Event('authStateChanged'));
}

// Token'ı localStorage'dan al
function getToken() {
    return localStorage.getItem('token');
}

// Token'ı localStorage'a kaydet
function setToken(token) {
    if (token) {
        localStorage.setItem('token', token);
    } else {
        localStorage.removeItem('token');
    }
    dispatchAuthStateChanged();
}

// Auth header'larını oluştur
async function getAuthHeaders() {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    return headers;
}

// Kullanıcının giriş yapmış olup olmadığını kontrol et
async function isAuthenticated() {
    const token = getToken();
    if (!token) return false;

    try {
        const response = await fetch('http://localhost:8000/auth/me', {
            headers: await getAuthHeaders(),
            credentials: 'include'
        });

        if (!response.ok) {
            setToken(null);
            return false;
        }

        return true;
    } catch (error) {
        console.error('Auth check error:', error);
        setToken(null);
        return false;
    }
}

// Giriş yap
async function login(email, password) {
    try {
        console.log('Login isteği gönderiliyor...');
        const formData = new URLSearchParams();
        formData.append('username', email);  // OAuth2 standardı gereği username olarak gönderiyoruz
        formData.append('password', password);

        const response = await fetch('http://localhost:8000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            },
            body: formData,
            credentials: 'include'
        });

        console.log('Login yanıtı:', {
            status: response.status,
            statusText: response.statusText,
            headers: Object.fromEntries(response.headers.entries())
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Giriş başarısız');
        }

        const data = await response.json();
        setToken(data.access_token);
        dispatchAuthStateChanged();
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// Kayıt ol
async function register(username, email, password) {
    try {
        console.log('Register isteği gönderiliyor...');
        const response = await fetch('http://localhost:8000/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ username, email, password }),
            credentials: 'include'
        });

        console.log('Register yanıtı:', {
            status: response.status,
            statusText: response.statusText,
            headers: Object.fromEntries(response.headers.entries())
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Kayıt başarısız');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Register error:', error);
        throw error;
    }
}

// Çıkış yap
async function logout() {
    try {
        const token = getToken();
        if (token) {
            const response = await fetch('http://localhost:8000/auth/logout', {
                method: 'POST',
                headers: await getAuthHeaders(),
                credentials: 'include'
            });

            if (!response.ok) {
                console.warn('Logout API error:', response.status);
            }
        }
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        setToken(null);
        dispatchAuthStateChanged();
    }
}

// Mevcut kullanıcı bilgilerini getir
async function getCurrentUser() {
    try {
        const response = await fetch('http://localhost:8000/auth/me', {
            headers: await getAuthHeaders(),
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Kullanıcı bilgileri alınamadı');
        }

        return await response.json();
    } catch (error) {
        console.error('Get current user error:', error);
        throw error;
    }
}

// Auth nesnesini dışa aktar
const auth = {
    login,
    register,
    logout,
    isAuthenticated,
    getCurrentUser,
    getAuthHeaders
};

// Sayfa yüklendiğinde form işlemlerini ve sayfa erişim kontrollerini ayarla
document.addEventListener('DOMContentLoaded', async () => {
    // Sayfa erişim kontrolü
    const currentPath = window.location.pathname;
    const publicPages = ['/', '/index.html', '/login.html', '/register.html'];
    const isPublicPage = publicPages.includes(currentPath);

    try {
        const isAuthenticated = await auth.isAuthenticated();

        if (!isPublicPage && !isAuthenticated) {
            // Korumalı sayfalara giriş yapmadan erişmeye çalışılırsa login sayfasına yönlendir
            window.location.href = '/login.html';
            return;
        }

        if (isPublicPage && isAuthenticated) {
            // Giriş yapmış kullanıcı login veya register sayfalarına erişmeye çalışırsa ana sayfaya yönlendir
            if (currentPath === '/login.html' || currentPath === '/register.html') {
                window.location.href = '/';
                return;
            }
        }
    } catch (error) {
        console.error('Auth check error:', error);
        if (!isPublicPage) {
            window.location.href = '/login.html';
            return;
        }
    }

    // Login formu
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                await auth.login(email, password);
                window.location.href = '/';
            } catch (error) {
                alert(error.message || 'Giriş işlemi başarısız oldu');
            }
        });
    }

    // Register formu
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                await auth.register(username, email, password);
                await auth.login(email, password);
                window.location.href = '/';
            } catch (error) {
                alert(error.message || 'Kayıt işlemi başarısız oldu');
            }
        });
    }

    // Story üret butonu için kontrol
    const storyButton = document.getElementById('createStoryButton');
    if (storyButton) {
        storyButton.addEventListener('click', (e) => {
            if (!auth.isAuthenticated()) {
                e.preventDefault();
                window.location.href = '/login.html';
            }
        });
    }
});

// Export auth object
window.auth = auth; 