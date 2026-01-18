document.addEventListener('DOMContentLoaded', () => {

    const formulario = document.getElementById('formulario');
    const btnEnviar = document.getElementById('btnEnviar');
    const btnResetear = document.getElementById('btnResetear'); 
    
    // Lista de inputs 
    const inputs = {
        nombre: document.getElementById('nombre'),
        correo: document.getElementById('correo'),
        edad: document.getElementById('edad'),
        contrasena: document.getElementById('contrasena'), 
        confirmarContrasena: document.getElementById('confirmarContrasena') 
    };

    // 2. Reglas (Expresiones Regulares)
    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const regexPass = /^(?=.*\d)(?=.*[\W_]).{8,}$/; // 8 chars, 1 num, 1 simbolo

    // Estado de validación
    const validacion = {
        nombre: false,
        correo: false,
        edad: false,
        contrasena: false,
        confirmarContrasena: false
    };

    // 3. Función para pintar verde/rojo
    const validarCampo = (input, esValido, mensaje) => {
        const idSpan = 'error' + input.id.charAt(0).toUpperCase() + input.id.slice(1);
        const span = document.getElementById(idSpan);
        
        if (esValido) {
            input.classList.remove('invalido');
            input.classList.add('valido');
            span.textContent = ""; 
        } else {
            input.classList.remove('valido');
            input.classList.add('invalido');
            span.textContent = mensaje; 
        }
    };

    // 4. Validaciones
    const checkNombre = () => {
        if (inputs.nombre.value.trim().length >= 3) {
            validarCampo(inputs.nombre, true);
            validacion.nombre = true;
        } else {
            validarCampo(inputs.nombre, false, "Mínimo 3 caracteres");
            validacion.nombre = false;
        }
        checkBoton();
    };

    const checkCorreo = () => {
        if (regexEmail.test(inputs.correo.value)) {
            validarCampo(inputs.correo, true);
            validacion.correo = true;
        } else {
            validarCampo(inputs.correo, false, "Correo inválido");
            validacion.correo = false;
        }
        checkBoton();
    };

    const checkEdad = () => {
        if (inputs.edad.value >= 18) {
            validarCampo(inputs.edad, true);
            validacion.edad = true;
        } else {
            validarCampo(inputs.edad, false, "Debes ser mayor de 18");
            validacion.edad = false;
        }
        checkBoton();
    };

    const checkContrasena = () => {
        if (regexPass.test(inputs.contrasena.value)) {
            validarCampo(inputs.contrasena, true);
            validacion.contrasena = true;
        } else {
            validarCampo(inputs.contrasena, false, "Mínimo 8 chars, 1 número, 1 símbolo");
            validacion.contrasena = false;
        }
        checkConfirmar(); 
        checkBoton();
    };

    const checkConfirmar = () => {
        const pass1 = inputs.contrasena.value;
        const pass2 = inputs.confirmarContrasena.value;

        if (pass1 === pass2 && pass1 !== "") {
            validarCampo(inputs.confirmarContrasena, true);
            validacion.confirmarContrasena = true;
        } else {
            validarCampo(inputs.confirmarContrasena, false, "No coinciden");
            validacion.confirmarContrasena = false;
        }
        checkBoton();
    };

    const checkBoton = () => {
        const todoOk = Object.values(validacion).every(v => v === true);
        btnEnviar.disabled = !todoOk;
    };

    // 5. Eventos 
    inputs.nombre.addEventListener('input', checkNombre);
    inputs.correo.addEventListener('input', checkCorreo);
    inputs.edad.addEventListener('input', checkEdad);
    inputs.contrasena.addEventListener('input', checkContrasena);
    inputs.confirmarContrasena.addEventListener('input', checkConfirmar);

    // Resetear
    btnResetear.addEventListener('click', () => {
        formulario.reset();
        Object.values(inputs).forEach(i => i.classList.remove('valido', 'invalido'));
        document.querySelectorAll('.error-mensaje').forEach(s => s.textContent = "");
        btnEnviar.disabled = true;
        for (let key in validacion) validacion[key] = false;
    });
});