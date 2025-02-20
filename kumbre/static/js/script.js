let currentIndex = 0;
        const slides = document.querySelectorAll('.slide');
        
        function changeSlide() {
            slides[currentIndex].classList.remove('active');
            currentIndex = (currentIndex + 1) % slides.length;
            slides[currentIndex].classList.add('active');
        }
        
        setInterval(changeSlide, 4000); // Cambia cada 4 segundos

// Inicia el carrusel al cargar la página
updateCarousel();
startAutoPlay();
