document.addEventListener('DOMContentLoaded', function() {
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    const slide = document.querySelector('.slide');
    const items = document.querySelectorAll('.slide .item');
    
    // Índice de la imagen actualmente visible en móviles
    // Iniciamos en 0 para mostrar la primera imagen automáticamente
    let currentMobileIndex = 0;
    
    // Función para comprobar si estamos en vista móvil
    function isMobileView() {
        return window.innerWidth <= 867;
    }
    
    // Función para actualizar la visualización en modo móvil
    function updateMobileView() {
        if (isMobileView()) {
            // Ocultar todas las imágenes
            items.forEach((item) => {
                item.style.display = 'none';
                item.classList.remove('active-mobile');
            });
            
            // Mostrar solo la imagen actual
            items[currentMobileIndex].style.display = 'block';
            items[currentMobileIndex].classList.add('active-mobile');
            
            // Hacer visible el contenido
            if (items[currentMobileIndex].querySelector('.content')) {
                items[currentMobileIndex].querySelector('.content').style.display = 'block';
            }
        } else {
            // Restaurar la visualización normal para escritorio
            items.forEach(item => {
                item.style.display = '';
                item.classList.remove('active-mobile');
            });
        }
    }
    
    // Inicializar la vista inmediatamente
    updateMobileView();
    
    // Manejar el botón "Siguiente"
    nextBtn.addEventListener('click', function() {
        if (isMobileView()) {
            // Incrementar el índice y manejar el ciclo
            currentMobileIndex = (currentMobileIndex + 1) % items.length;
            updateMobileView();
        } else {
            // Comportamiento original del slider para escritorio
            let firstItem = slide.firstElementChild;
            slide.appendChild(firstItem);
        }
    });
    
    // Manejar el botón "Anterior"
    prevBtn.addEventListener('click', function() {
        if (isMobileView()) {
            // Decrementar el índice y manejar el ciclo
            currentMobileIndex = (currentMobileIndex - 1 + items.length) % items.length;
            updateMobileView();
        } else {
            // Comportamiento original del slider para escritorio
            let lastItem = slide.lastElementChild;
            slide.prepend(lastItem);
        }
    });
    
    // Volver a calcular cuando cambie el tamaño de la ventana
    window.addEventListener('resize', updateMobileView);
});