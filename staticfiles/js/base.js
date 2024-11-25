// Función para manejar el toggle del sidebar
document.getElementById('sidebarToggle').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('show');
});

// Detectar el enlace activo basado en la URL actual
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.nav-link');
    
    links.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Cerrar sidebar en móvil al hacer clic en un enlace
if (window.innerWidth <= 768) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            document.getElementById('sidebar').classList.remove('show');
        });
    });
}