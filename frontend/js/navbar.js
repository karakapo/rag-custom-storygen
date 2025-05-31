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
            // Navbar yüklendikten sonra butonları güncelle ve aktif sayfayı işaretle
            loadNavbar();
        } else {
            console.error('Navbar container bulunamadı');
        }
    } catch (error) {
        console.error('Navbar yükleme hatası:', error);
    }
}

// Navbar'ı yükle ve aktif sayfayı işaretle
async function loadNavbar() {
    console.log('Navbar yükleniyor...');

    // Aktif sayfayı belirle
    const currentPath = window.location.pathname;
    const navLinks = {
        '/': 'navHome',
        '/index.html': 'navHome',
        '/create.html': 'navCreate',
        '/profile.html': 'navProfile'
    };

    // Aktif linki işaretle
    const activeLinkId = navLinks[currentPath];
    if (activeLinkId) {
        const activeLink = document.getElementById(activeLinkId);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }

    // Auth durumunu kontrol et
    await updateAuthButtons();
}

// Auth durumuna göre butonları güncelle
async function updateAuthButtons() {
    console.log('Auth butonları güncelleniyor...');
    const authButtons = document.getElementById('authButtons');
    const userButtons = document.getElementById('userButtons');
    const navCreate = document.getElementById('navCreate');
    const navProfile = document.getElementById('navProfile');

    if (!authButtons || !userButtons) {
        console.error('Auth butonları bulunamadı');
        return;
    }

    try {
        // Authentication durumunu kontrol et
        const isAuthenticated = await auth.isAuthenticated();
        console.log('Auth durumu:', isAuthenticated);

        if (isAuthenticated) {
            // Kullanıcı giriş yapmışsa
            authButtons.style.display = 'none';
            userButtons.style.display = 'flex';
            if (navCreate) navCreate.style.display = 'block';
            if (navProfile) navProfile.style.display = 'block';
        } else {
            // Kullanıcı giriş yapmamışsa
            authButtons.style.display = 'flex';
            userButtons.style.display = 'none';
            if (navCreate) navCreate.style.display = 'none';
            if (navProfile) navProfile.style.display = 'none';
        }
    } catch (error) {
        console.error('Auth check error:', error);
        // Hata durumunda varsayılan olarak giriş yapmamış durumu göster
        authButtons.style.display = 'flex';
        userButtons.style.display = 'none';
        if (navCreate) navCreate.style.display = 'none';
        if (navProfile) navProfile.style.display = 'none';
    }
}

// Çıkış yapma işlemini yönet
async function handleLogout() {
    try {
        await auth.logout();
        window.location.href = '/';
    } catch (error) {
        console.error('Logout error:', error);
        alert('Çıkış yapılırken bir hata oluştu');
    }
}

// Sayfa yüklendiğinde navbar'ı yükle
document.addEventListener('DOMContentLoaded', loadNavbarComponent);

// Auth durumu değiştiğinde butonları güncelle
window.addEventListener('authStateChanged', updateAuthButtons); 