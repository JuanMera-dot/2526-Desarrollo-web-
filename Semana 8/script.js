//Funcionalidad del Botón de Sorpresa (Descuento)
document.getElementById('btnAlerta').addEventListener('click', function() {
    
    //Mostrar la alerta inicial
    alert("¡Felicidades! Has obtenido el 10% de descuento en tu primera compra.");

    // Seleccionar todas las filas de productos de la tabla
    let filas = document.querySelectorAll('table tbody tr');

    //Recorrer cada fila para cambiar el precio
    filas.forEach(function(fila) {
        let celdaPrecio = fila.cells[4]; 

        // Verificamos si ya aplicamos el descuento para no aplicarlo dos veces si dan clic de nuevo
        if (!celdaPrecio.classList.contains('descuento-aplicado')) {
            
            let textoPrecio = celdaPrecio.innerText;
            let precioNumerico = parseFloat(textoPrecio.replace('$', ''));
            let nuevoPrecio = (precioNumerico * 0.90).toFixed(2); //deja solo 2 decimales

            //Actualizar el HTML de la celda
            celdaPrecio.innerHTML = `
                <span style="text-decoration: line-through; color: red;">${textoPrecio}</span>
                <span style="font-weight: bold; color: green; margin-left: 5px;">$${nuevoPrecio}</span>
                <div style="font-size: 0.65rem; color: gray; margin-top: 2px; line-height: 1.1;">
                    *aplica solo para la primera compra en un solo articulo
                </div>
            `;
            celdaPrecio.classList.add('descuento-aplicado');
        }
    });
});

//Validación del Formulario (Esto se mantiene igual que antes)
document.getElementById('formularioContacto').addEventListener('submit', function(evento) {
    evento.preventDefault(); // Evitar envío automático

    let nombre = document.getElementById('nombre').value;
    let email = document.getElementById('email').value;
    let mensaje = document.getElementById('mensaje').value;
    let valido = true;

    // Limpiar errores
    document.getElementById('errorNombre').textContent = "";
    document.getElementById('errorEmail').textContent = "";
    document.getElementById('errorMensaje').textContent = "";

    // Validaciones
    if (nombre.trim() === "") {
        document.getElementById('errorNombre').textContent = "Por favor, escribe tu nombre.";
        valido = false;
    }

    if (email.trim() === "" || !email.includes('@')) {
        document.getElementById('errorEmail').textContent = "Ingresa un correo válido con @.";
        valido = false;
    }

    if (mensaje.trim() === "") {
        document.getElementById('errorMensaje').textContent = "El mensaje no puede estar vacío.";
        valido = false;
    }

    if (valido) {
        alert("¡Formulario enviado correctamente!");
        this.reset();
    }
});