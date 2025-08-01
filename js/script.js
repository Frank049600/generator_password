$(document).ready(function () {
    $('#formulario').on('submit', function(event) {
        event.preventDefault();
        var cantidad = $('input[name=cantidad]').val();
        var pwd_length = $('input[name=pwd_length]').val();
        var use_num = $('input[name=use_num]:checked').val();
        var use_caracterE = $('input[name=use_caracterE]:checked').val();
        var datos = {
            "cantidad": cantidad,
            "pwd_length": pwd_length,
            "use_num": use_num,
            "use_caracterE": use_caracterE,
        };
        // Se presenta la peticion ajax
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/pwd",
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify(datos),
            success: function (response) {
                $("#passwords").empty();
                $.each(response, function(index, pass) {
                    $("#passwords").append('<span>Contraseña: </span><span>"' + pass + '"</span><br>');
                });
            },
            error: function (xhr, status, error) {
                console.error("Error en la petición:", status, error);
            }
        });
    });
});