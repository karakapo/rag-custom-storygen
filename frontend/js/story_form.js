// Check authentication on page load
document.addEventListener('DOMContentLoaded', async () => {
    const isAuth = await auth.checkAuth();
    if (!isAuth) {
        window.location.href = 'login.html';
        return;
    }

    // Update user info in the header if needed
    const user = auth.getCurrentUser();
    if (user) {
        const userInfoElement = document.getElementById('userInfo');
        if (userInfoElement) {
            userInfoElement.textContent = user.email;
        }
    }
});

// Story form submission
document.getElementById('storyForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const user = auth.getCurrentUser();
    if (!user) {
        window.location.href = 'login.html';
        return;
    }

    // Form verilerini al
    const formData = {
        prompt: document.getElementById('prompt').value,
        user_id: user.id
    };

    try {
        // Backend'e POST isteği gönder
        const response = await fetch('http://localhost:8000/story/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Network response was not ok');
        }

        const result = await response.json();
        
        // Sonucu localStorage'a kaydet
        localStorage.setItem('currentStory', JSON.stringify(result));
        
        // Result sayfasına yönlendir
        window.location.href = 'result.html';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Hikaye oluşturulurken bir hata oluştu: ' + error.message);
    }
});

// Logout handler
document.getElementById('logoutBtn')?.addEventListener('click', async (e) => {
    e.preventDefault();
    try {
        await auth.logout();
    } catch (error) {
        console.error('Logout failed:', error);
        alert('Çıkış yapılırken bir hata oluştu');
    }
});

// Story type butonları
const btnTemplate = document.getElementById('btnTemplate');
const btnFree = document.getElementById('btnFree');
const storyTypeInput = document.getElementById('storyType');

btnTemplate.addEventListener('click', function() {
    storyTypeInput.value = '1';
    btnTemplate.classList.add('active');
    btnFree.classList.remove('active');
});

btnFree.addEventListener('click', function() {
    storyTypeInput.value = '0';
    btnFree.classList.add('active');
    btnTemplate.classList.remove('active');
}); 