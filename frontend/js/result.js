document.addEventListener('DOMContentLoaded', function() {
    // localStorage'dan hikayeyi al
    const storyData = JSON.parse(localStorage.getItem('currentStory'));
    
    if (storyData) {
        // Hikaye bilgilerini sayfaya yerleştir
        document.getElementById('storyTitle').textContent = storyData.title;
        document.getElementById('storyText').innerHTML = storyData.content.replace(/\n/g, '<br>');
        document.getElementById('createdAt').textContent = new Date(storyData.created_at).toLocaleDateString('tr-TR');
    } else {
        // Hikaye verisi yoksa ana sayfaya yönlendir
        window.location.href = 'index.html';
    }
});

// Yeni hikaye oluşturma fonksiyonu
function createNewStory() {
    window.location.href = 'create.html';
} 