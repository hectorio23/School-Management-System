const API_BASE_URL = 'http://127.0.0.1:8000/students'; // URL for authenticate using POST
const LOGIN_URL = `${API_BASE_URL}/login/`;
const VERIFY_URL = `${API_BASE_URL}/verify-token/`;

// Función para mostrar alertas
function showAlert(message, type = 'danger') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    document.body.appendChild(alert);

    setTimeout(() => {
        alert.style.animation = 'slideDown 0.3s ease-out reverse';
        setTimeout(() => alert.remove(), 300);
    }, 3000);
}

// Función para verificar token al cargar la página
async function verifySession() {
    const overlay = document.getElementById('loadingOverlay');
    const container = document.getElementById('loginContainer');
    
    // Mostrar overlay de carga
    overlay.classList.remove('hidden');
    container.style.opacity = '0';

    try {
        const response = await fetch(VERIFY_URL, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();


        if (response.ok && data.valid) {
            // Token valido, redirigir inmediatamente
            console.log('Sesión válida encontrada, redirigiendo...');
            window.location.href = 'http://127.0.0.1:8000/dashboard';
        } else {
            // Token invalido o no existe, mostrar formulario
            showLoginForm(overlay, container);
        }
    } catch (error) {
        console.error('Error verificando sesión:', error);
        // En caso de error, mostrar el login
        showLoginForm(overlay, container);
    }
}

// Función para mostrar el formulario de login
function showLoginForm(overlay, container) {
    overlay.classList.add('hidden');
    container.style.opacity = '1';
}

// Manejo del formulario de login
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const loginBtn = document.getElementById('loginBtn');
    
    // Deshabilitar boton y mostrar loading
    loginBtn.disabled = true;
    const originalText = loginBtn.textContent;
    loginBtn.innerHTML = '<span class="spinner"></span>Iniciando sesión...';

    try {
        const response = await fetch(LOGIN_URL, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                username: username,
                password: password 
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showAlert('¡Login exitoso! Redirigiendo...', 'success');
            console.log('Login exitoso:', data);

            console.log(data);
            
            // Redirigir inmediatamente
            setTimeout(() => {

                window.location.href = '/dashboard.html';
            }, 500);
        } else {
            // Error de login
            const errorMsg = data.error || 'Usuario o contraseña incorrectos';
            showAlert(errorMsg, 'danger');
            
            // Restaurar boton
            loginBtn.disabled = false;
            loginBtn.textContent = originalText;
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error de conexión con el servidor', 'danger');
        
        // Restaurar botón
        loginBtn.disabled = false;
        loginBtn.textContent = originalText;
    }
});

// Forgot password
document.getElementById('forgotLink').addEventListener('click', function(e) {
    e.preventDefault();
    showAlert('[+] - Funcionalidad en desarrollo :(', 'success');
});

// Verificar sesión al cargar la página
window.addEventListener('DOMContentLoaded', verifySession);