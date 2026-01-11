// static/js/login.js

// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:8000/api';
const AUTH_ENDPOINTS = {
    // Apunta al endpoint de SimpleJWT
    login: `${API_BASE_URL}/token/`,
};

// Utilidades para manejo de tokens (Cookies)
const TokenManager = {
    set(accessToken, refreshToken) {
        // Guardar cookies con path raíz y SameSite Strict
        document.cookie = `access_token=${accessToken}; path=/; SameSite=Strict`;
        document.cookie = `refresh_token=${refreshToken}; path=/; SameSite=Strict`;
    },

    getAccess() {
        return this.getCookie('access_token');
    },

    getRefresh() {
        return this.getCookie('refresh_token');
    },

    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    },

    clear() {
        document.cookie = "access_token=; path=/; max-age=0; SameSite=Strict";
        document.cookie = "refresh_token=; path=/; max-age=0; SameSite=Strict";
    },

    exists() {
        return !!this.getAccess();
    }
};

// Utilidades UI
const UI = {
    showLoading(message = 'Verificando sesión...') {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            const text = overlay.querySelector('.loading-text');
            if (text) text.textContent = message;
            overlay.classList.remove('hidden');
        }
    },

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.add('hidden');
        }
    },

    showError(message) {
        let errorDiv = document.querySelector('.error-message');

        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            const form = document.getElementById('loginForm');
            if (form) form.parentNode.insertBefore(errorDiv, form);
        }

        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
        }
    },

    clearError() {
        const errorDiv = document.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    },

    disableForm(disabled = true) {
        const form = document.getElementById('loginForm');
        if (form) {
            const inputs = form.querySelectorAll('input, button');
            inputs.forEach(input => {
                input.disabled = disabled;
            });
        }
    }
};

// API Service
const APIService = {
    async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const token = TokenManager.getAccess();
        if (token) {
            defaultOptions.headers['Authorization'] = `Bearer ${token}`;
        }

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                const errorMessage = data.detail || (data.password ? data.password[0] : null) || (data.email ? data.email[0] : null) || 'Error de autenticación';
                throw new Error(errorMessage);
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    async login(email, password) {
        return await this.request(AUTH_ENDPOINTS.login, {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    }
};

// Lógica de autenticación
const Auth = {
    async login(email, password) {
        UI.showLoading('Iniciando sesión...');
        UI.disableForm(true);
        UI.clearError();

        try {
            const response = await APIService.login(email, password);

            if (response.access && response.refresh) {
                TokenManager.set(response.access, response.refresh);

                UI.showLoading('Login exitoso. Redirigiendo...');

                setTimeout(() => {
                    window.location.href = 'http://127.0.0.1:8000/students/dashboard';
                }, 1000);
            } else {
                throw new Error('Respuesta inválida del servidor');
            }

        } catch (error) {
            UI.hideLoading();
            UI.disableForm(false);
            UI.showError(error.message || 'Error al iniciar sesión. Verifica tus credenciales.');
        }
    }
};

// Lógica de Inicialización (Manejo de Sesión y Navegación)
function initLogin() {
    // 1. Verificar si hay sesión activa
    if (TokenManager.exists()) {
        console.log('Sesión detectada. Redirigiendo al dashboard...');
        window.location.href = 'http://127.0.0.1:8000/students/dashboard';
        return;
    }

    // 2. Si NO hay sesión, asegurar estado limpio (importante para Back button)
    UI.hideLoading();
    UI.disableForm(false);

    // 3. Mostrar formulario con animación
    const loginContainer = document.getElementById('loginContainer');
    if (loginContainer) {
        loginContainer.style.opacity = '0';
        loginContainer.style.display = 'block';
        requestAnimationFrame(() => {
            loginContainer.style.transition = 'opacity 0.3s';
            loginContainer.style.opacity = '1';
        });
    }

    // 4. Setup Listeners (Idempotente)
    const loginForm = document.getElementById('loginForm');
    if (loginForm && !loginForm.dataset.initialized) {
        loginForm.dataset.initialized = 'true';
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;

            if (!email || !password) {
                UI.showError('Por favor completa todos los campos');
                return;
            }

            await Auth.login(email, password);
        });
    }

    const forgotLink = document.getElementById('forgotLink');
    if (forgotLink && !forgotLink.dataset.initialized) {
        forgotLink.dataset.initialized = 'true';
        forgotLink.addEventListener('click', (e) => {
            e.preventDefault();
            alert('Funcionalidad no implementada en esta demo.');
        });
    }
}

// Ejecutar al cargar el DOM
document.addEventListener('DOMContentLoaded', initLogin);

// Modificación Clave: Manejar BFCache (Back/Forward Cache)
// Esto soluciona el problema de volver atrás y ver la página en estado de carga
window.addEventListener('pageshow', (event) => {
    // Si la página viene del cache (persisted) o si hay token al volver
    if (event.persisted || TokenManager.exists()) {
        console.log('Page show event (persisted or token exists). Re-initializing...');
        initLogin();
    }
});