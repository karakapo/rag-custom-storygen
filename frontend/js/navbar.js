// Navbar'ı yükle
async function loadNavbarComponent() {
    try {
        const response = await fetch('/navbar.html');
        if (!response.ok) {
            throw new Error('Navbar yüklenemedi');
        }
        const html = await response.text();
        
        // Navbar'ı sayfaya ekle
        const navbarContainer = document.getElementById('navbar-container');
        if (navbarContainer) {
            navbarContainer.innerHTML = html;
            // Navbar yüklendikten sonra aktif sayfayı işaretle
            loadNavbar();
        } else {
            console.error('Navbar container bulunamadı');
        }
    } catch (error) {
        console.error('Navbar yükleme hatası:', error);
    }
}

// Navbar'ı yükle ve aktif sayfayı işaretle
function loadNavbar() {
    console.log('Navbar yükleniyor...');

    // Aktif sayfayı belirle
    const currentPath = window.location.pathname;
    const navLinks = {
        '/': 'navHome',
        '/index.html': 'navHome',
        '/create.html': 'navCreate'
    };

    // Aktif linki işaretle
    const activeLinkId = navLinks[currentPath];
    if (activeLinkId) {
        const activeLink = document.getElementById(activeLinkId);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }
}

// Sayfa yüklendiğinde navbar'ı yükle
document.addEventListener('DOMContentLoaded', loadNavbarComponent); 