document.getElementById('openModalBtn1').addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña1');
    modal.style.display = "block";
});

document.getElementById('openModalBtn2').addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña2');
    modal.style.display = "block";
});

document.getElementById('openModalBtn3').addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña3');
    modal.style.display = "block";
});

document.getElementById('openModalBtn4').addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña4');
    modal.style.display = "block";
});

document.getElementById('openModalBtn5').addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña5');
    modal.style.display = "block";
});



// Cerrar modales
document.getElementById('modalCabaña1').getElementsByClassName('close')[0].addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña1');
    modal.style.display = "none";
});


document.getElementById('modalCabaña2').getElementsByClassName('close')[0].addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña2');
    modal.style.display = "none";
});


document.getElementById('modalCabaña3').getElementsByClassName('close')[0].addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña3');
    modal.style.display = "none";
});


document.getElementById('modalCabaña4').getElementsByClassName('close')[0].addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña4');
    modal.style.display = "none";
});


document.getElementById('modalCabaña5').getElementsByClassName('close')[0].addEventListener('click', function() {
    var modal = document.getElementById('modalCabaña5');
    modal.style.display = "none";
});

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-pane");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].className = tabcontent[i].className.replace(" active", "");
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).className += " active";
    evt.currentTarget.className += " active";
}



// Función para configurar modales y sliders para múltiples cabañas
function setupCabinModalAndSlider(cabinNumber) {
    // Get the modal
    var modal = document.getElementById(`modalCabaña${cabinNumber}`);

    // Get the <span> element that closes the modal
    var span = document.querySelector(`#modalCabaña${cabinNumber} .close`);

    // Get slides for this specific cabin
    let slides = document.querySelectorAll(`#modalCabaña${cabinNumber} .slide`);
    let currentSlide = 0;

    // Initialize first slide
    if (slides.length > 0) {
        slides[currentSlide].classList.add('active');
    }

    // Optional: Add button to open modal if needed
    // var btn = document.getElementById(`openCabinModal${cabinNumber}`);
    // if (btn) {
    //     btn.onclick = function() {
    //         modal.style.display = "block";
    //     }
    // }

    // Close modal when clicking on (x)
    if (span) {
        span.onclick = function() {
            modal.style.display = "none";
        }
    }

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    // Next slide button
    let nextButton = document.querySelector(`#modalCabaña${cabinNumber} .next-button`);
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        });
    }

    // Previous slide button
    let prevButton = document.querySelector(`#modalCabaña${cabinNumber} .prev-button`);
    if (prevButton) {
        prevButton.addEventListener('click', () => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');
        });
    }
}

// Configurar modales y sliders para 5 cabañas
document.addEventListener('DOMContentLoaded', () => {
    for (let i = 1; i <= 5; i++) {
        setupCabinModalAndSlider(i);
    }
});



// Get the modal
var modal = document.getElementById("modalCabaña2");

// Get the button that opens the modal
// (Añade un botón para abrir el modal si no tienes uno)
// var btn = document.getElementById("myBtn");
// btn.onclick = function() {
//     modal.style.display = "block";
// }

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


document.querySelector('.next-button').addEventListener('click', () => {
    slides[currentSlide].classList.remove('active');
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].classList.add('active');
});

document.querySelector('.prev-button').addEventListener('click', () => {
    slides[currentSlide].classList.remove('active');
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
});




document.addEventListener('DOMContentLoaded', function() {
    // Event listeners for opening modals
    for (let i = 1; i <= 5; i++) {
        const openBtn = document.getElementById(`openModalBtn${i}`);
        if (openBtn) {
            openBtn.addEventListener('click', function() {
                const modal = document.getElementById(`modalCabaña${i}`);
                if (modal) {
                    modal.style.display = "block";
                    
                    // Reset slides to first slide when opening modal
                    const slides = modal.querySelectorAll('.slide');
                    slides.forEach((slide, index) => {
                        slide.classList.remove('active');
                        if (index === 0) slide.classList.add('active');
                    });
                    
                    // Prevent body scrolling when modal is open
                    document.body.style.overflow = 'hidden';
                }
            });
        }
    }

    // Event listeners for closing modals
    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(function(closeBtn) {
        closeBtn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.display = "none";
                // Re-enable body scrolling
                document.body.style.overflow = 'auto';
            }
        });
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = "none";
            // Re-enable body scrolling
            document.body.style.overflow = 'auto';
        }
    });

    // Setup slider functionality for each cabin
    function setupSlider(cabinNumber) {
        const modal = document.getElementById(`modalCabaña${cabinNumber}`);
        if (!modal) return;
        
        const slides = modal.querySelectorAll('.slide');
        let currentSlide = 0;
        
        // Initialize first slide
        if (slides.length > 0) {
            slides[currentSlide].classList.add('active');
        }
        
        // Next slide button
        const nextButton = modal.querySelector('.next-button');
        if (nextButton) {
            nextButton.addEventListener('click', () => {
                slides[currentSlide].classList.remove('active');
                currentSlide = (currentSlide + 1) % slides.length;
                slides[currentSlide].classList.add('active');
            });
        }
        
        // Previous slide button
        const prevButton = modal.querySelector('.prev-button');
        if (prevButton) {
            prevButton.addEventListener('click', () => {
                slides[currentSlide].classList.remove('active');
                currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                slides[currentSlide].classList.add('active');
            });
        }
        
        // Touch swipe support for mobile devices
        let touchStartX = 0;
        let touchEndX = 0;
        
        const sliderContainer = modal.querySelector('.slider-container');
        if (sliderContainer) {
            sliderContainer.addEventListener('touchstart', (e) => {
                touchStartX = e.changedTouches[0].screenX;
            }, {passive: true});
            
            sliderContainer.addEventListener('touchend', (e) => {
                touchEndX = e.changedTouches[0].screenX;
                handleSwipe();
            }, {passive: true});
        }
        
        function handleSwipe() {
            const swipeThreshold = 50;
            if (touchEndX < touchStartX - swipeThreshold) {
                // Swipe left - next slide
                if (nextButton) nextButton.click();
            } else if (touchEndX > touchStartX + swipeThreshold) {
                // Swipe right - previous slide
                if (prevButton) prevButton.click();
            }
        }
    }

    // Setup sliders for all 5 cabins
    for (let i = 1; i <= 5; i++) {
        setupSlider(i);
    }
    
    // Handle window resize events to adjust layout
    function handleResize() {
        const windowWidth = window.innerWidth;
        const galleryItems = document.querySelectorAll('.gallery-item');
        
        if (windowWidth <= 480) {
            // For very small screens, show fewer gallery items
            galleryItems.forEach((item, index) => {
                if (index >= 2) {
                    item.style.display = 'none';
                } else {
                    item.style.display = 'block';
                }
            });
        } else {
            // Show all gallery items
            galleryItems.forEach(item => {
                item.style.display = 'block';
            });
        }
    }
    
    // Initial call and event listener for resize
    handleResize();
    window.addEventListener('resize', handleResize);
});