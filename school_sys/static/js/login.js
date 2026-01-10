// static/js/login.js

// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:8000/api';
const AUTH_ENDPOINTS = {
    login: `${API_BASE_URL}/auth/login/`,
    verify: `${API_BASE_URL}/auth/verify/`,
};

// Utilidades para manejo de tokens
const TokenManager = {
    set(accessToken, refreshToken) {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
    },
    
    getAccess() {
        return localStorage.getItem('access_token');
    },
    
    getRefresh() {
        return localStorage.getItem('refresh_token');
    },
    
    clear() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
        localStorage.removeItem('redirect_info');
    },
    
    exists() {
        return !!this.getAccess();
    }
};

// Utilidades para manejo de usuario
const UserManager = {
    set(userData) {
        localStorage.setItem('user_data', JSON.stringify(userData));
    },
    
    get() {
        const data = localStorage.getItem('user_data');
        return data ? JSON.parse(data) : null;
    },
    
    getRole() {
        const user = this.get();
        return user ? user.role : null;
    },
    
    isAdmin() {
        return this.getRole() === 'admin';
    },
    
    isStudent() {
        return this.getRole() === 'student';
    }
};

// Utilidades para redirección
const RedirectManager = {
    set(redirectInfo) {
        localStorage.setItem('redirect_info', JSON.stringify(redirectInfo));
    },
    
    get() {
        const data = localStorage.getItem('redirect_info');
        return data ? JSON.parse(data) : null;
    },
    
    getDashboardUrl() {
        const info = this.get();
        return info ? info.dashboard_url : null;
    },
    
    redirect() {
        const dashboardUrl = this.getDashboardUrl();
        if (dashboardUrl) {
            window.location.href = dashboardUrl;
        }
    }
};

// Utilidades UI
const UI = {
    showLoading(message = 'Verificando sesión...') {
        const overlay = document.getElementById('loadingOverlay');
        const text = overlay.querySelector('.loading-text');
        text.textContent = message;
        overlay.classList.remove('hidden');
    },
    
    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.classList.add('hidden');
    },
    
    showError(message) {
        // Crear o actualizar mensaje de error
        let errorDiv = document.querySelector('.error-message');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            const form = document.getElementById('loginForm');
            form.parentNode.insertBefore(errorDiv, form);
        }
        
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    },
    
    clearError() {
        const errorDiv = document.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    },
    
    disableForm(disabled = true) {
        const form = document.getElementById('loginForm');
        const inputs = form.querySelectorAll('input, button');
        inputs.forEach(input => {
            input.disabled = disabled;
        });
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
        
        // Agregar token si existe
        const token = TokenManager.getAccess();
        if (token) {
            defaultOptions.headers['Authorization'] = `Bearer ${token}`;
        }
        
        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `Error: ${response.status}`);
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
    },
    
    async verifyToken() {
        return await this.request(AUTH_ENDPOINTS.verify, {
            method: 'GET'
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
            
            if (response.success) {
                // Guardar tokens
                TokenManager.set(response.access, response.refresh);
                
                // Guardar datos de usuario
                UserManager.set(response.user);
                
                // Guardar info de redirección
                RedirectManager.set(response.redirect);
                
                // Log para debugging
                console.log('Login exitoso:', {
                    role: response.user.role,
                    redirect: response.redirect.dashboard_url
                });
                
                // Mostrar mensaje de éxito
                console.log(response.user)
                UI.showLoading(`¡Bienvenido ${response.user.nombre}! Redirigiendo...`);
                
                // Redirigir después de 1 segundo
                setTimeout(() => {
                    RedirectManager.redirect();
                }, 10000);
            } else {
                throw new Error('Respuesta de login inválida');
            }
            
        } catch (error) {
            UI.hideLoading();
            UI.disableForm(false);
            UI.showError(error.message || 'Error al iniciar sesión. Verifica tus credenciales.');
            console.error('Login error:', error);
        }
    },
    
    async verifySession() {
        // Si no hay token, no verificar
        if (!TokenManager.exists()) {
            return false;
        }
        
        UI.showLoading('Verificando sesión...');
        
        try {
            const response = await APIService.verifyToken();
            
            if (response.valid) {
                // Sesión válida, redirigir al dashboard
                console.log('Sesión válida, redirigiendo...');
                RedirectManager.redirect();
                return true;
            }
        } catch (error) {
            console.log('Token inválido o expirado:', error);
            // Token inválido, limpiar y mostrar login
            TokenManager.clear();
        }
        
        UI.hideLoading();
        return false;
    },
    
    logout() {
        TokenManager.clear();
        window.location.href = '/';
    }
};

// Inicialización cuando carga el DOM
document.addEventListener('DOMContentLoaded', async () => {
    // Verificar si ya hay sesión activa
    const hasValidSession = await Auth.verifySession();
    
    if (hasValidSession) {
        // Ya se redirigió, no hacer nada más
        return;
    }
    
    // No hay sesión, mostrar formulario de login
    const loginForm = document.getElementById('loginForm');
    const loginContainer = document.getElementById('loginContainer');
    
    // Mostrar el contenedor de login
    loginContainer.style.opacity = '0';
    loginContainer.style.display = 'block';
    setTimeout(() => {
        loginContainer.style.transition = 'opacity 0.3s';
        loginContainer.style.opacity = '1';
    }, 100);
    
    // Manejar submit del formulario
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
    
    // Manejar link de "olvidé contraseña" (opcional)
    const forgotLink = document.getElementById('forgotLink');
    if (forgotLink) {
        forgotLink.addEventListener('click', (e) => {
            e.preventDefault();
            alert('Funcionalidad de recuperación de contraseña en desarrollo');
            // Aquí puedes redirigir a una página de recuperación
            // window.location.href = '/reset-password/';
        });
    }
});

// Exponer Auth globalmente para debugging
window.Auth = Auth;
window.TokenManager = TokenManager;
window.UserManager = UserManager;