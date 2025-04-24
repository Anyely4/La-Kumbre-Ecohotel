document.addEventListener('DOMContentLoaded', function() {
    // Funciones para manejar los modales
    function setupModal(btnId, modalId) {
        var btn = document.getElementById(btnId);
        var modal = document.getElementById(modalId);
        var span = modal.querySelector(".close");
        
        btn.onclick = function() {
            modal.style.display = "block";
            document.body.style.overflow = "hidden"; // Previene el scroll del body
            
            // Reinicia el slider al abrir el modal
            var slides = modal.querySelectorAll('.slide');
            slides.forEach(function(slide) {
                slide.classList.remove('active');
            });
            slides[0].classList.add('active');
        }
        
        span.onclick = function() {
            modal.style.display = "none";
            document.body.style.overflow = "auto"; // Añade esta línea
        }
        
        window.addEventListener('click', function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
                 document.body.style.overflow = "auto"; // Añade esta línea
              
            }
        });
        
        // Configuración de los botones de navegación del slider
        var prevBtn = modal.querySelector('.prev-button');
        var nextBtn = modal.querySelector('.next-button');
        var slides = modal.querySelectorAll('.slide');
        
        prevBtn.addEventListener('click', function() {
            var activeSlide = modal.querySelector('.slide.active');
            var prevSlide = activeSlide.previousElementSibling || slides[slides.length - 1];
            
            activeSlide.classList.remove('active');
            prevSlide.classList.add('active');
        });
        
        nextBtn.addEventListener('click', function() {
            var activeSlide = modal.querySelector('.slide.active');
            var nextSlide = activeSlide.nextElementSibling || slides[0];
            
            activeSlide.classList.remove('active');
            nextSlide.classList.add('active');
        });
    }
    
    // Configuración de los carruseles de imágenes
    function setupCarousels() {
        var carousels = document.querySelectorAll('.carousel');
        
        carousels.forEach(function(carousel) {
            var images = carousel.querySelector('.carousel-images');
            var imageWidth = images.offsetWidth / 2; // Cada imagen ocupa 50% del ancho
            
            // Configuración específica para móviles
            function updateCarousel() {
                if (window.innerWidth <= 992) {
                    // En móviles, el hover no funciona bien, así que aplicamos manualmente la animación
                    carousel.addEventListener('click', function() {
                        if (images.style.transform === 'translateX(-50%)') {
                            images.style.transition = 'transform 0.5s ease-in-out';
                            images.style.transform = 'translateX(0)';
                        } else {
                            images.style.transition = 'transform 0.5s ease-in-out';
                            images.style.transform = 'translateX(-50%)';
                        }
                    });
                } else {
                    // En escritorio, usamos el hover normal
                    images.style.transform = '';
                    images.style.transition = '';
                }
            }
            
            // Inicializar y actualizar en cada cambio de tamaño
            updateCarousel();
            window.addEventListener('resize', updateCarousel);
        });
    }
    
    // Inicialización de modales
    setupModal('openModalBtn1', 'modalCabaña1');
    setupModal('openModalBtn2', 'modalCabaña2');
    setupModal('openModalBtn3', 'modalCabaña3');
    setupModal('openModalBtn4', 'modalCabaña4');
    setupModal('openModalBtn5', 'modalCabaña5');
    
    // Inicialización de carruseles
    setupCarousels();
});