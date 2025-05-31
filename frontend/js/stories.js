// API endpoint'leri
const API_BASE_URL = 'http://localhost:8000';

// Hikaye işlemleri
const stories = {
    // Yeni hikaye oluştur
    createStory: async (title, content) => {
        try {
            const response = await fetch(`${API_BASE_URL}/stories/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, content })
            });

            if (!response.ok) {
                throw new Error('Hikaye oluşturulamadı');
            }

            return await response.json();
        } catch (error) {
            console.error('Error creating story:', error);
            throw error;
        }
    },

    // Kullanıcının hikayelerini getir
    getUserStories: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/stories/user`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Hikayeler yüklenemedi');
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching stories:', error);
            throw error;
        }
    },

    // Son hikayeleri getir
    getRecentStories: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/stories/recent`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Hikayeler yüklenemedi');
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching recent stories:', error);
            throw error;
        }
    },

    // Hikaye detaylarını getir
    getStoryDetails: async (storyId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/stories/${storyId}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Hikaye detayları yüklenemedi');
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching story details:', error);
            throw error;
        }
    }
};

// Sayfa yüklendiğinde hikayeleri yükle
document.addEventListener('DOMContentLoaded', async () => {
    // Hikaye oluşturma formu
    const storyForm = document.getElementById('storyForm');
    if (storyForm) {
        storyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const title = document.getElementById('storyTitle').value;
            const content = document.getElementById('storyContent').value;
            
            try {
                await stories.createStory(title, content);
                alert('Hikaye başarıyla oluşturuldu!');
                window.location.reload();
            } catch (error) {
                alert('Hikaye oluşturulurken bir hata oluştu: ' + error.message);
            }
        });
    }

    // Son hikayeleri yükle
    const recentStoriesContainer = document.getElementById('recentStories');
    if (recentStoriesContainer) {
        try {
            const stories = await stories.getRecentStories();
            if (stories.length === 0) {
                recentStoriesContainer.innerHTML = '<p class="text-muted">Henüz hiç hikaye yok.</p>';
                return;
            }

            const storiesHTML = stories.map(story => `
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title">${story.title}</h5>
                        <p class="card-text">${story.content.substring(0, 150)}...</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">${new Date(story.created_at).toLocaleDateString('tr-TR')}</small>
                            <a href="/story.html?id=${story.id}" class="btn btn-primary btn-sm">Devamını Oku</a>
                        </div>
                    </div>
                </div>
            `).join('');

            recentStoriesContainer.innerHTML = storiesHTML;
        } catch (error) {
            recentStoriesContainer.innerHTML = '<p class="text-danger">Hikayeler yüklenirken bir hata oluştu.</p>';
        }
    }
}); 