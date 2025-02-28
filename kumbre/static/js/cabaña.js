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



