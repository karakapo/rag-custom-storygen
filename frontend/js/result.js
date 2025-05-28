document.addEventListener('DOMContentLoaded', function() {
    // localStorage'dan hikayeyi al
    const storyData = JSON.parse(localStorage.getItem('currentStory'));
    
    if (storyData) {
        // Hikaye bilgilerini sayfaya yerleştir
        document.getElementById('characterName').textContent = storyData.name;
        document.getElementById('characterAge').textContent = storyData.age;
        document.getElementById('storyGenre').textContent = storyData.genre;
        document.getElementById('storyText').innerHTML = storyData.content.replace(/\n/g, '<br>');
    } else {
        // Hikaye verisi yoksa ana sayfaya yönlendir
        window.location.href = 'index.html';
    }
});

// Hikayeyi kaydetme fonksiyonu
async function saveStory() {
    const storyData = JSON.parse(localStorage.getItem('currentStory'));
    
    try {
        const response = await fetch('http://localhost:8000/story/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(storyData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Network response was not ok');
        }

        alert('Hikaye başarıyla kaydedildi!');
        window.location.href = 'profile.html';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Hikaye kaydedilirken bir hata oluştu: ' + error.message);
    }
} 