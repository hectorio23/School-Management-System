import { useState } from 'react';
import { useNavigate, Navigate, Link } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { ROLE_ROUTES } from '../constants/roles';

export default function Login() {
    const { login, isAuthenticated, user } = useAuth();
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    // If already logged in, redirect
    if (isAuthenticated && user) {
        return <Navigate to={ROLE_ROUTES[user.role] || '/'} replace />;
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const result = await login(email, password);

            if (result.mfa_required) {
                navigate('/mfa-verify');
            } else if (result.success) {
                navigate(ROLE_ROUTES[result.role] || '/');
            }
        } catch (err) {
            const detail = err.response?.data?.detail || err.response?.data?.error;
            if (detail) {
                setError(typeof detail === 'string' ? detail : JSON.stringify(detail));
            } else if (err.response?.data) {
                // Handle validation errors from SimpleJWT
                const data = err.response.data;
                const msgs = Object.values(data).flat();
                setError(msgs.join(' '));
            } else {
                setError('Error de conexión. Verifica que el servidor esté activo.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            <div className="login-card">
                <div className="login-header">
                    {/* Ícono open-source: Academic Cap — Heroicons (MIT License) https://heroicons.com */}
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                        className="login-logo"
                        style={{ color: 'var(--primary)', width: 64, height: 64 }}
                        aria-label="Sistema de Gestión Institucional"
                    >
                        <path d="M11.7 2.805a.75.75 0 0 1 .6 0A60.65 60.65 0 0 1 22.83 8.72a.75.75 0 0 1-.231 1.337 49.948 49.948 0 0 0-9.902 3.912l-.003.002c-.114.06-.227.119-.34.18a.75.75 0 0 1-.707 0A50.88 50.88 0 0 0 7.5 12.173v-.224c0-.131.067-.248.172-.311a54.615 54.615 0 0 1 4.653-2.52.75.75 0 0 0-.65-1.352 56.123 56.123 0 0 0-4.78 2.589 1.858 1.858 0 0 0-.859 1.228 49.803 49.803 0 0 0-4.634-1.527.75.75 0 0 1-.231-1.337A60.653 60.653 0 0 1 11.7 2.805Z" />
                        <path d="M13.06 15.473a48.45 48.45 0 0 1 7.666-3.282c.134 1.414.22 2.843.255 4.284a.75.75 0 0 1-.46.71 47.87 47.87 0 0 1-8.105 2.874.75.75 0 0 1-.505 0 47.867 47.867 0 0 1-8.105-2.874.75.75 0 0 1-.46-.71c.035-1.44.121-2.87.255-4.284a48.45 48.45 0 0 1 7.666 3.282c.38.194.802.294 1.225.294.424 0 .845-.1 1.224-.294Z" />
                        <path d="M15.75 17.5v3.75a.75.75 0 0 1-1.5 0V17.5l.75.5.75-.5Z" />
                    </svg>
                    <h1 className="login-title">Sistema de Gestión Intitucional</h1>
                    <p className="login-subtitle">Ingresa tus credenciales para continuar</p>
                </div>

                {error && (
                    <div className="alert alert-error" style={{ marginBottom: '20px' }}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label" htmlFor="email">
                            Correo electrónico / matricula
                        </label>
                        <input
                            id="email"
                            type="text"
                            className="form-input"
                            placeholder="usuario@escuela.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            autoComplete="email"
                            autoFocus
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="password">
                            Contraseña
                        </label>
                        <input
                            id="password"
                            type="password"
                            className="form-input"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            autoComplete="current-password"
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary login-btn"
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <div className="spinner" style={{ width: 18, height: 18, borderWidth: 2 }} />
                                Ingresando...
                            </>
                        ) : (
                            'Iniciar Sesión'
                        )}
                    </button>
                </form>

                <div style={{ marginTop: '20px', textAlign: 'center' }}>
                    <Link to="/forgot-password" style={{ color: 'var(--primary)', textDecoration: 'none', fontSize: '14px' }}>
                        ¿Olvidaste tu contraseña?{' '}
                    </Link>
                </div>
            </div>
        </div>
    );
}
