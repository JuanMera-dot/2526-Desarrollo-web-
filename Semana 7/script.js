// 1. ARREGLO DE DATOS
const prendas = [
    { nombre: "Camisa oficina", precio: 30.00, descripcion: "Camisa formal para oficina"},
    { nombre: "Pantalón jeans", precio: 45.00, descripcion: "Pantalón de mezclilla casual"},
    { nombre: "Vestido verano", precio: 60.00, descripcion: "Vestido ligero para verano"},
    { nombre: "Chaqueta cuero", precio: 120.00, descripcion: "Chaqueta de cuero elegante"},
    { nombre: "Falda lápiz", precio: 35.00, descripcion: "Falda ajustada para oficina"},
];

// 2. SELECCIÓN DE ELEMENTOS
const contenedorPrendas = document.getElementById("lista-productos");
const botonAgregar = document.getElementById("agregar");

// 3. FUNCIÓN PARA RENDERIZAR
function mostrarPrendas() {
    contenedorPrendas.innerHTML = "";
    
    prendas.forEach((prenda, index) => {
        const item = document.createElement("li");

        item.innerHTML = `
            <div>
                <strong>${prenda.nombre}</strong> - $${prenda.precio} <br>
                <small>${prenda.descripcion}</small>
            </div>
            <button onclick="editarPrenda(${index})" style="margin-left: 10px; cursor:pointer;"> Editar</button>
        `;

        // Estilos para que se vea ordenado
        item.style.display = "flex";
        item.style.justifyContent = "space-between";
        item.style.marginBottom = "10px";
        item.style.padding = "10px";
        item.style.borderBottom = "1px solid #ccc";
        
        contenedorPrendas.appendChild(item);
    });
}

// . FUNCIÓN PARA AGREGAR
function agregarPrenda() {
    const nuevaPrenda = {
        nombre: "Nueva prenda",
        precio: 50.00,
        descripcion: "Descripción pendiente"
    };
    prendas.push(nuevaPrenda);
    mostrarPrendas();
}

// 5. FUNCIÓN PARA EDITAR
function editarPrenda(i) {
    // Buscamos la prenda específica usando el índice (i)
    let prendaActual = prendas[i];

    // Pedimos los nuevos datos
    let nuevoNombre = prompt("Editar nombre:", prendaActual.nombre);
    let nuevoPrecio = prompt("Editar precio:", prendaActual.precio);
    let nuevaDesc = prompt("Editar descripción:", prendaActual.descripcion);

    // Si el usuario escribió algo en los 3 campos, guardamos
    if (nuevoNombre && nuevoPrecio && nuevaDesc) {
        prendas[i].nombre = nuevoNombre;
        prendas[i].precio = parseFloat(nuevoPrecio);
        prendas[i].descripcion = nuevaDesc;
        
        mostrarPrendas(); // Actualizamos la pantalla
    }
}

// 6. EVENTOS
if (botonAgregar) {
    botonAgregar.addEventListener("click", agregarPrenda);
}

// INICIALIZAR
mostrarPrendas();