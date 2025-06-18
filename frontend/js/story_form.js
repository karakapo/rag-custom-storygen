// Story form submission
document.addEventListener('DOMContentLoaded', () => {
    const storyForm = document.getElementById('storyForm');
    if (storyForm) {
        storyForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Form verilerini al
            const formData = {
                prompt: document.getElementById('prompt').value
            };

            try {
                // Backend'e POST isteği gönder
                const response = await fetch('http://localhost:8000/story/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
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
    }
});

// Story type butonları
document.addEventListener('DOMContentLoaded', () => {
    const btnTemplate = document.getElementById('btnTemplate');
    const btnFree = document.getElementById('btnFree');
    const storyTypeInput = document.getElementById('storyType');

    if (btnTemplate && btnFree && storyTypeInput) {
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
    }
}); 