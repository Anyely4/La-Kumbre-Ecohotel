const carousel = document.querySelector('.carrusel'); 
const slides = document.querySelectorAll('.fotos'); 
const prevButton = document.querySelector('.prev'); 
const nextButton = document.querySelector('.next'); 

let currentIndex = 0; 
let autoPlayInterval; // Para almacenar el intervalo de autoplay

// Función para actualizar el carrusel
function updateCarousel() {
    const width = slides[0].clientWidth; // Calcula el ancho de cada slide
    carousel.style.transform = `translateX(-${currentIndex * width}px)`; // Desplaza el carrusel
}

// Función para ir al siguiente slide
function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length; // Avanza al siguiente slide
    updateCarousel();
}

// Función para ir al slide anterior
function prevSlide() {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length; // Regresa al slide anterior
    updateCarousel();
}

// Iniciar autoplay
function startAutoPlay() {
    autoPlayInterval = setInterval(() => {
        nextSlide(); // Avanza automáticamente al siguiente slide
    }, 4000); // Cambia cada 3 segundos
}

// Pausar autoplay
function stopAutoPlay() {
    clearInterval(autoPlayInterval); // Detiene el intervalo
}

// Escucha de eventos para los botones de control
nextButton.addEventListener('click', () => {
    stopAutoPlay(); // Pausa el autoplay para dar control al usuario
    nextSlide(); // Pasa al siguiente slide
    startAutoPlay(); // Reinicia el autoplay después de un clic
});

prevButton.addEventListener('click', () => {
    stopAutoPlay(); // Pausa el autoplay para dar control al usuario
    prevSlide(); // Va al slide anterior
    startAutoPlay(); // Reinicia el autoplay después de un clic
});

// Inicia el carrusel al cargar la página
updateCarousel();
startAutoPlay();
