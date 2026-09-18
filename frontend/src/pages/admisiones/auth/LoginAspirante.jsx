
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../../auth/AuthContext';
import { HiOutlineAcademicCap } from 'react-icons/hi';
import api from '../../../api/client';

export default function LoginAspirante() {
    const { loginAspirante } = useAuth(); // New method we'll add to AuthContext
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await loginAspirante(email, password);
            // Redirection is handled in AuthContext or here if needed, 
            // but let's assume AuthContext updates state and we redirect based on user role
            navigate('/aspirante/dashboard');
        } catch (err) {
            console.error("Login error:", err);
            const detail = err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || 'Error al iniciar sesión';
            setError(typeof detail === 'string' ? detail : JSON.stringify(detail));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page aspirant-theme">
            <div className="login-card">
                <div className="login-header">
                    <HiOutlineAcademicCap className="login-logo" style={{ fontSize: '32px', color: '#ffffff' }} />
                    <h1 className="login-title">Portal de Aspirantes</h1>
                    <p className="login-subtitle">Inicia sesión para continuar tu proceso de admisión</p>
                </div>

                {error && (
                    <div className="alert alert-error mb-3">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Correo Electrónico</label>
                        <input
                            type="email"
                            className="form-input"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="tucorreo@ejemplo.com"
                            required
                            autoFocus
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Contraseña</label>
                        <input
                            type="password"
                            className="form-input"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary login-btn"
                        disabled={loading}
                    >
                        {loading ? 'Ingresando...' : 'Iniciar Sesión'}
                    </button>
                </form>

                <div className="mt-3 text-center">
                    <p className="text-sm text-muted">
                        ¿Aún no tienes cuenta?{' '}
                        <Link to="/aspirantes/registro" className="text-primary font-medium">
                            Regístrate aquí
                        </Link>
                    </p>
                </div>
            </div>

            <style>{`
                .aspirant-theme {
                    background-color: #cbd5e1;
                    background: 
                      radial-gradient(ellipse at 85% 15%, rgba(148, 163, 184, 0.45) 0%, transparent 60%),
                      radial-gradient(ellipse at 15% 85%, rgba(71, 85, 105, 0.35) 0%, transparent 60%),
                      radial-gradient(circle at 50% 50%, rgba(248, 250, 252, 0.4) 0%, transparent 75%),
                      linear-gradient(140deg, #e2e8f0 0%, #cbd5e1 35%, #94a3b8 70%, #64748b 100%);
                }
                .aspirant-theme::before {
                    content: '';
                    position: absolute;
                    inset: 0;
                    background-image: radial-gradient(rgba(255, 255, 255, 0.3) 1.2px, transparent 1.2px);
                    background-size: 26px 26px;
                    opacity: 0.7;
                    pointer-events: none;
                }
                .aspirant-logo {
                    background: linear-gradient(135deg, #475569 0%, #1e293b 100%);
                    color: #ffffff;
                }
                .text-primary {
                    color: #334155;
                }
                .text-primary:hover {
                    color: #0f172a;
                    text-decoration: underline;
                }
            `}</style>
        </div>
    );
}
