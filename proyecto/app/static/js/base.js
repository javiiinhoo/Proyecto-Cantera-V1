// obtén todos los botones que desencadenan el colapso
var botones = document.querySelectorAll('[data-toggle="collapse"]');

// recorre cada botón y agrega un controlador de eventos clic
botones.forEach(function (boton) {
    boton.addEventListener('click', function () {
        // obtén el objetivo del botón
        var objetivo = document.querySelector(this.getAttribute('data-target'));

        // agrega o elimina la clase "show" del objetivo para mostrar u ocultar el contenido
        if (objetivo.classList.contains('show')) {
            objetivo.classList.add('d-none');
            objetivo.classList.remove('show');
        } else {
            objetivo.classList.remove('d-none');
            objetivo.classList.add('show');
        }
    });
});
