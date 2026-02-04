// static/js/login.js

// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:8000/api';
const AUTH_ENDPOINTS = {
    login: `${API_BASE_URL}/token/`,
    verifyMFA: `${API_BASE_URL}/token/mfa-verify/`,
};
// Utilidades para manejo de tokens (Cookies)
const TokenManager = {
    is_admin: false,
    set(accessToken, refreshToken) {
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
    },

    showModal(message, duration = 3000) {
        let modal = document.getElementById('alertModal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'alertModal';
            modal.className = 'modal-overlay';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-icon">!</div>
                    <p class="modal-message"></p>
                </div>
            `;
            document.body.appendChild(modal);
        }

        const messageEl = modal.querySelector('.modal-message');
        if (messageEl) messageEl.textContent = message;

        modal.style.display = 'flex';

        setTimeout(() => {
            modal.style.display = 'none';
        }, duration);
    }
};

// Gestor de MFA
const MFAManager = {
    expiryTime: null,
    timerInterval: null,
    email: null,

    show(email, expiredAt) {
        this.email = email;
        this.expiryTime = new Date(expiredAt);

        // Ocultar formulario de login
        const loginContainer = document.getElementById('loginContainer');
        if (loginContainer) loginContainer.style.display = 'none';

        // Crear o mostrar formulario MFA
        let mfaContainer = document.getElementById('mfaContainer');
        if (!mfaContainer) {
            mfaContainer = this.createMFAForm();
            document.body.appendChild(mfaContainer);
        }

        mfaContainer.style.display = 'flex';

        // Iniciar temporizador
        this.startTimer();

        // Focus en el input
        const codeInput = document.getElementById('mfaCode');
        if (codeInput) {
            codeInput.value = '';
            codeInput.focus();
        }
    },

    createMFAForm() {
        const container = document.createElement('div');
        container.id = 'mfaContainer';
        container.className = 'mfa-container';
        container.innerHTML = `
            <div class="mfa-card">
                <div class="mfa-header">
                    <h2>
                        <span>🔐</span>
                        Autenticación de Dos Factores
                    </h2>
                    <p>Hemos enviado un código de verificación de 6 dígitos a tu correo electrónico registrado</p>
                </div>
                
                <div class="mfa-timer">
                    <div class="timer-icon">⏱️</div>
                    <div class="timer-text">
                        Tiempo restante: <span id="mfaTimer">02:00</span>
                    </div>
                </div>

                <form id="mfaForm" autocomplete="off">
                    <div class="mfa-input-group">
                        <input 
                            type="text" 
                            id="mfaCode" 
                            name="mfaCode"
                            maxlength="6" 
                            pattern="[0-9]{6}"
                            inputmode="numeric"
                            placeholder="000000"
                            autocomplete="off"
                            required
                        />
                    </div>

                    <div class="error-message mfa-error" style="display: none;"></div>

                    <button type="submit" class="mfa-submit-btn">
                        Verificar Código
                    </button>

                    <button type="button" class="mfa-cancel-btn" id="mfaCancelBtn">
                        Volver al inicio de sesión
                    </button>
                </form>

                <div class="security-badge">
                    <span class="security-badge-icon">*</span>
                    <span class="security-badge-text">Tu información está protegida y encriptada</span>
                </div>
            </div>`
            ;

        // Agregar listener para solo permitir números en el input
        setTimeout(() => {
            const codeInput = container.querySelector('#mfaCode');
            if (codeInput) {
                codeInput.addEventListener('input', (e) => {
                    e.target.value = e.target.value.replace(/[^0-9]/g, '');
                });
            }
        }, 0);

        return container;
    },

    startTimer() {
        this.updateTimerDisplay();

        this.timerInterval = setInterval(() => {
            const now = new Date();
            const remaining = this.expiryTime - now;

            if (remaining <= 0) {
                this.handleExpiry();
            } else {
                this.updateTimerDisplay();
            }
        }, 1000);
    },

    updateTimerDisplay() {
        const now = new Date();
        const remaining = Math.max(0, this.expiryTime - now);

        const minutes = Math.floor(remaining / 60000);
        const seconds = Math.floor((remaining % 60000) / 1000);

        const timerEl = document.getElementById('mfaTimer');
        if (timerEl) {
            timerEl.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

            // Cambiar color si queda poco tiempo
            if (remaining < 30000) {
                timerEl.style.color = '#dc3545';
            }
        }
    },

    handleExpiry() {
        this.cleanup();

        // Mostrar modal de tiempo expirado
        UI.showModal('⏰ Tiempo expirado. Por favor inicia sesión nuevamente.', 3000);

        // Volver al login después del modal
        setTimeout(() => {
            this.hide();
            const loginContainer = document.getElementById('loginContainer');
            if (loginContainer) loginContainer.style.display = 'block';
        }, 3000);
    },

    cleanup() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    },

    hide() {
        this.cleanup();
        const mfaContainer = document.getElementById('mfaContainer');
        if (mfaContainer) mfaContainer.style.display = 'none';
    },

    showMFAError(message) {
        const errorDiv = document.querySelector('.mfa-error');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
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
            credentials: 'include',
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);

            // Intentar parsear JSON
            let data;
            try {
                data = await response.json();
            } catch (e) {
                data = {};
            }

            if (!response.ok) {
                const errorMessage = data.detail ||
                    data.error ||
                    (data.password ? data.password[0] : null) ||
                    (data.email ? data.email[0] : null) ||
                    'Error de autenticación';
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
    },

    async verifyMFA(email, code) {
        return await this.request(AUTH_ENDPOINTS.verifyMFA, {
            method: 'POST',
            body: JSON.stringify({ email, code })
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

            // Caso 1: MFA requerido (Admin)
            if (response.mfa_required) {
                UI.hideLoading();
                UI.disableForm(false);
                MFAManager.show(email, response.expired_at);
                return;
            }

            // Caso 2: Login directo exitoso (Estudiante)
            if (response.access && response.refresh) {
                TokenManager.set(response.access, response.refresh);
                UI.showLoading('Login exitoso. Redirigiendo...');

                // Redirigir según el rol o URL del response
                setTimeout(() => {
                    if (response.redirect && response.redirect.dashboard_url) {
                        window.location.href = response.redirect.dashboard_url;
                    } else {
                        // Fallback por si no viene redirect
                        window.location.href = '/students/dashboard';
                    }
                }, 1000);
            } else {
                throw new Error('Respuesta inválida del servidor');
            }

        } catch (error) {
            UI.hideLoading();
            UI.disableForm(false);
            UI.showError(error.message || 'Error al iniciar sesión. Verifica tus credenciales.');
        }
    },

    async verifyMFA(email, code) {
        UI.showLoading('Verificando código...');

        try {
            const response = await APIService.verifyMFA(email, code);

            // Verificar si recibimos los tokens
            if (response.access && response.refresh) {
                TokenManager.set(response.access, response.refresh);
                MFAManager.cleanup();

                UI.showLoading('Autenticación exitosa. Redirigiendo...');

                setTimeout(() => {
                    // Admin siempre va a /api/admin/dashboard
                    window.location.href = '/api/admin/dashboard';
                }, 1000);
            } else {
                throw new Error('Respuesta inválida del servidor');
            }

        } catch (error) {
            UI.hideLoading();

            // Si el error es "Invalid or expired code", mostrar en el formulario MFA
            if (error.message.includes('Invalid') || error.message.includes('expired')) {
                MFAManager.showMFAError(error.message);
            } else {
                // Otros errores, volver al login
                MFAManager.hide();
                const loginContainer = document.getElementById('loginContainer');
                if (loginContainer) loginContainer.style.display = 'block';
                UI.showError(error.message);
            }
        }
    }
};

// Lógica de Inicialización
function initLogin() {
    // 1. Verificar si hay sesión activa
    if (TokenManager.exists() && TokenManager.is_admin) {
        console.log('Sesión detectada. Redirigiendo al dashboard...');
        window.location.href = '/students/dashboard';
        return;
    }

    // 2. Estado limpio
    UI.hideLoading();
    UI.disableForm(false);

    // 3. Mostrar formulario de login
    const loginContainer = document.getElementById('loginContainer');
    if (loginContainer) {
        loginContainer.style.opacity = '0';
        loginContainer.style.display = 'block';
        requestAnimationFrame(() => {
            loginContainer.style.transition = 'opacity 0.3s';
            loginContainer.style.opacity = '1';
        });
    }

    // 4. Setup Login Form Listener
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

    // 5. Setup MFA Form Listener (delegado)
    document.addEventListener('submit', async (e) => {
        if (e.target.id === 'mfaForm') {
            e.preventDefault();

            const code = document.getElementById('mfaCode').value.trim();

            if (!/^\d{6}$/.test(code)) {
                MFAManager.showMFAError('El código debe tener 6 dígitos numéricos');
                return;
            }

            await Auth.verifyMFA(MFAManager.email, code);
        }
    });

    // 6. Cancelar MFA
    document.addEventListener('click', (e) => {
        if (e.target.id === 'mfaCancelBtn') {
            MFAManager.hide();
            const loginContainer = document.getElementById('loginContainer');
            if (loginContainer) loginContainer.style.display = 'block';
        }
    });

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

// Manejar BFCache
window.addEventListener('pageshow', (event) => {
    if (event.persisted || TokenManager.exists()) {
        console.log('Page show event. Re-initializing...');
        initLogin();
    }
});