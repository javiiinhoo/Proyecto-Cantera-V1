$(function () {
    var hoy = new Date();
    var ultima_actualizacion = new Date("2023-01-01"); // reemplazar con la fecha de la última actualización de los jugadores
    var meses_pasados = (hoy.getFullYear() - ultima_actualizacion.getFullYear()) * 12 + (hoy.getMonth() - ultima_actualizacion.getMonth());

    if (meses_pasados >= 2) {
        alert("Han pasado más de 2 meses desde la última actualización de jugadores. Por favor importe jugadores.");
        window.location.href = "{% url 'importar_jugadores' %}";
        return;
    }

    var jugadores = [];
    for (var i = 0; i < players.length; i++) {
        var jugador = players[i];
        jugadores.push({
            label: jugador.nombre,
            value: jugador.id
        });
    }

    if (jugadores.length === 0) {
        alert("No hay jugadores disponibles. Por favor importe jugadores.");
        window.location.href = "{% url 'importar_jugadores' %}";
        return;
    }

    $("#buscar-jugador").autocomplete({
        source: jugadores,
        minLength: 2,
        select: function (event, ui) {
            $("#jugadores").val(ui.item.value);
        }
    });

    $("#jugadores").on("change", function () {
        var jugador_id = $(this).val();
        if (jugador_id) {
            window.location.href = "{% url 'jugador_detalle' %}?id=" + jugador_id;
        }
    });
});