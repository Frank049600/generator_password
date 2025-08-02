$(document).ready(function () {
    $('#formulario').on('submit', function (event) {
        // Detiene el envio de datos
        event.preventDefault();
        var cantidad = $('input[name=cantidad]').val();
        var pwd_length = $('input[name=pwd_length]').val();
        var use_num = $('input[name=use_num]:checked').val();
        var use_caracterE = $('input[name=use_caracterE]:checked').val();
        $('#alojados').empty().hide(100);
        // Validación de datos
        $('#msg').empty();
        if (cantidad < 1 || cantidad > 10) {
            $('#msg').append('<span>' +
                'Puedes solicitar de 1 a 10 contraseñas' +
                '</span>').show(300);
            return false;
        } else if (pwd_length < 10 || pwd_length > 17) {
            $('#msg').append('<span>' +
                'Puedes definir un tamaño entre 10 y 17 caracteres' +
                '</span>').show(300);
            return false;
        }
        var datos = {
            "cantidad": cantidad,
            "pwd_length": pwd_length,
            "use_num": use_num,
            "use_caracterE": use_caracterE
        }
        var params = JSON.stringify(datos);

        fetch('https://generator-pasword.onrender.com/pwd', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: params
        })
            .then(response => response.json())
            .then(data => {
                // Muestra las contraseñas en la vista web
                $.each(data, function (index, pass) {
                    $('#alojados').append('<div class="pwd"><span>Contraseña: " <b id="pwd_' + index + '">' + pass + '</b> "</span><br>' +
                        '<button class="btn_copiar" id="btn_' + index + '" onclick="copiar(' + index + ')">Copiar</button></div>'
                    );
                });
                $('#alojados').append('<br><span><b>Nota</b>: Use la(s) contraseña(s) de dentro de las comillas dobles ("")</span><br>');
                $('#alojados').show(300);
            })
            .catch(error => {
                console.log(error);
            });
    });
    // Restablece los campos
    $('#restart').on('click', function () {
        restart();
    });

    window.onbeforeunload = function (e) {
        restart();
    };
});
// Función para realizar copiado de contraseñas
function copiar(pwd) {
    $('#btn_' + pwd).empty();
    $('#btn_' + pwd).append('Copiado');
    $('#btn_' + pwd).attr('style', 'color:green;');

    var texto = $('#pwd_' + pwd).text();
    navigator.clipboard.writeText(texto)
        .then(() => {
            console.log('Copiado');
            /* Resuelto - texto copiado al portapapeles con éxito */
        }, () => {
            console.error('Error al copiar');
            /* Rechazado - fallo al copiar el texto al portapapeles */
        });
}

function restart() {
    $('#alojados').empty().hide(100);
    $('input[name=cantidad]').val('');
    $('input[name=pwd_length]').val('');
    $('input[name="use_num"][value="si"]').prop('checked', true);
    $('input[name="use_caracterE"][value="si"]').prop('checked', true);
}