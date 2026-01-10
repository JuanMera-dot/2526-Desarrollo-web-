/* CACHÉ DE ELEMENTOS
   Guardamos los elementos en variables const).

*/
const inputUrl = document.getElementById('urlInput');
const btnAgregar = document.getElementById('btnAgregar');
const btnEliminar = document.getElementById('btnEliminar');
const galeria = document.getElementById('galeria');


/* FUNCIÓN PARA AGREGAR IMAGENES*/
function agregarImagen() {
    const url = inputUrl.value; // obtiene el texto escrito

    if (url === "") {
        alert("¡Escribe algo primero!");
        return; //  detiene la función, no sigue ejecutando.
    }

   
    // document.createElement('img') crea una etiqueta <img> en la memoria,.
    const nuevaImagen = document.createElement('img');
    
    // Le asignamos atributos
    nuevaImagen.src = url; 
    nuevaImagen.alt = "Imagen de galería";

    // su evento 'click' justo aquí, al momento de nacer.
    nuevaImagen.addEventListener('click', function() {
        // Cuando alguien haga clic en ESTA imagen específica, ejecutamos esto:
        seleccionarImagen(nuevaImagen);
    });

    // dentro del div de la galería. Ahora ya es visible.
    galeria.appendChild(nuevaImagen);

    inputUrl.value = ""; // Limpiamos el campo de texto
}


/*  FUNCIÓN PARA SELECCIONAR */
function seleccionarImagen(imagenClickeada) {
    // 1. Buscamos si hay alguna imagen que YA tenga la clase seleccionada.
    const imagenAnterior = document.querySelector('.seleccionada');

    // 2. Si existe una anterior, le quitamos la clase (le quitamos el borde azul).
    if (imagenAnterior) {
        imagenAnterior.classList.remove('seleccionada');
    }

    // 3. A la nueva imagen que clickeamos, le ponemos la clase (ponemos borde azul).
    imagenClickeada.classList.add('seleccionada');
}


/* FUNCIÓN PARA ELIMINAR */
function eliminarImagen() {
    // Buscamos quién tiene la clase seleccionada
    const imagenParaBorrar = document.querySelector('.seleccionada');

    if (imagenParaBorrar) {
        imagenParaBorrar.remove();
    } else {
        alert("No has seleccionado ninguna imagen para borrar.");
    }
}


/* CONECTAR BOTONES CON FUNCIONES */
btnAgregar.addEventListener('click', agregarImagen);
btnEliminar.addEventListener('click', eliminarImagen);