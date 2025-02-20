document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("infoModal");
    var btn = document.getElementById("openModalBtn");
    var closeBtn = document.querySelector(".close"); 
    
    if (!modal || !btn || !closeBtn) {
        console.error("Uno o más elementos no fueron encontrados.");
        return;
    }
    modal.style.display = "none";

    // Abrir el modal
    btn.addEventListener("click", function () {
        modal.style.display = "flex";
    });

    // Cerrar el modal al hacer clic en la "X"
    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Cerrar el modal al hacer clic fuera del contenido
    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});

