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
