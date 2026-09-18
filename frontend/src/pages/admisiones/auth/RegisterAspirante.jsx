
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { HiOutlineAcademicCap, HiOutlineUserAdd } from 'react-icons/hi';
import api from '../../../api/client';

export default function RegisterAspirante() {
    const navigate = useNavigate();
    const [step, setStep] = useState(1); // 1: Initiate (Email), 2: Confirm (Code + Details)
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [debugCode, setDebugCode] = useState(''); // Added for simulation

    // Step 1 Data
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    // Step 2 Data
    const [code, setCode] = useState('');
    const [nombre, setNombre] = useState('');
    const [apellidoPaterno, setApellidoPaterno] = useState('');
    const [apellidoMaterno, setApellidoMaterno] = useState('');
    const [curp, setCurp] = useState('');
    const [nivelIngreso, setNivelIngreso] = useState('PRIMARIA');

    const handleInitiate = async (e) => {
        e.preventDefault();
        setError('');

        if (password !== confirmPassword) {
            setError('Las contraseñas no coinciden');
            return;
        }

        setLoading(true);
        try {
            const res = await api.post('/api/admission/register/initiate/', { email, password });
            if (res.data.code_debug) {
                setDebugCode(res.data.code_debug);
            }
            setStep(2);
            setError('');
        } catch (err) {
            console.error("Registration initiation error:", err);
            const detail = err.response?.data?.detail || 'Error al iniciar registro';
            setError(typeof detail === 'string' ? detail : JSON.stringify(detail));
        } finally {
            setLoading(false);
        }
    };

    const handleConfirm = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const payload = {
                email,
                code,
                nombre,
                apellido_paterno: apellidoPaterno,
                apellido_materno: apellidoMaterno,
                curp,
                nivel_ingreso: nivelIngreso
            };
            await api.post('/api/admission/register/confirm/', payload);

            // Success! Redirect to login
            navigate('/aspirantes/login', {
                state: { message: 'Registro exitoso. Por favor inicia sesión.' }
            });
        } catch (err) {
            console.error("Registration confirmation error:", err);
            const detail = err.response?.data?.detail || 'Error al confirmar registro';
            setError(typeof detail === 'string' ? detail : JSON.stringify(detail));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page aspirant-theme">
            <div className="login-card" style={{ maxWidth: '480px' }}>
                <div className="login-header">
                    <div className="login-logo aspirant-logo">
                        <HiOutlineUserAdd />
                    </div>
                    <h1 className="login-title">Registro de Aspirantes</h1>
                    <p className="login-subtitle">
                        {step === 1
                            ? "Ingresa tu correo para comenzar el proceso"
                            : "Verifica tu correo y completa tus datos"}
                    </p>
                </div>

                {error && (
                    <div className="alert alert-error mb-3">
                        {error}
                    </div>
                )}

                {step === 1 ? (
                    <form onSubmit={handleInitiate}>
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
                                placeholder="Mínimo 8 caracteres"
                                minLength={8}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label className="form-label">Confirmar Contraseña</label>
                            <input
                                type="password"
                                className="form-input"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="Repite tu contraseña"
                                minLength={8}
                                required
                            />
                        </div>

                        <button
                            type="submit"
                            className="btn btn-primary login-btn"
                            disabled={loading}
                        >
                            {loading ? 'Enviando...' : 'Continuar'}
                        </button>
                    </form>
                ) : (
                    <form onSubmit={handleConfirm}>
                        <div className="text-center mb-4 p-3 bg-blue-50 text-blue-700 rounded-md text-sm">
                            Hemos enviado un código de verificación a <strong>{email}</strong>
                            {debugCode && (
                                <div className="mt-2 p-2 bg-yellow-100 border border-yellow-200 text-yellow-800 rounded font-mono font-bold">
                                    [SIMULACIÓN] Código: {debugCode}
                                </div>
                            )}
                        </div>

                        <div className="form-group">
                            <label className="form-label">Código de Verificación</label>
                            <input
                                type="text"
                                className="form-input text-center tracking-widest font-bold"
                                value={code}
                                onChange={(e) => setCode(e.target.value)}
                                placeholder="000000"
                                maxLength={6}
                                required
                                autoFocus
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                            <div className="form-group">
                                <label className="form-label">Nombre(s)</label>
                                <input
                                    type="text"
                                    className="form-input"
                                    value={nombre}
                                    onChange={(e) => setNombre(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">Apellido Paterno</label>
                                <input
                                    type="text"
                                    className="form-input"
                                    value={apellidoPaterno}
                                    onChange={(e) => setApellidoPaterno(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                            <div className="form-group">
                                <label className="form-label">Apellido Materno</label>
                                <input
                                    type="text"
                                    className="form-input"
                                    value={apellidoMaterno}
                                    onChange={(e) => setApellidoMaterno(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">CURP</label>
                                <input
                                    type="text"
                                    className="form-input uppercase"
                                    value={curp}
                                    onChange={(e) => setCurp(e.target.value.toUpperCase())}
                                    placeholder="ABCD123456HGTMTR01"
                                    maxLength={18}
                                    required
                                />
                            </div>
                        </div>

                        <div className="form-group mb-4">
                            <label className="form-label">Nivel de Ingreso</label>
                            <select
                                className="form-input"
                                value={nivelIngreso}
                                onChange={(e) => setNivelIngreso(e.target.value)}
                                required
                            >
                                <option value="PREESCOLAR">Preescolar</option>
                                <option value="PRIMARIA">Primaria</option>
                                <option value="SECUNDARIA">Secundaria</option>
                            </select>
                        </div>

                        <button
                            type="submit"
                            className="btn btn-primary login-btn"
                            disabled={loading}
                        >
                            {loading ? 'Registrando...' : 'Finalizar Registro'}
                        </button>
                    </form>
                )}

                <div className="mt-3 text-center">
                    <p className="text-sm text-muted">
                        ¿Ya tienes cuenta?{' '}
                        <Link to="/aspirantes/login" className="text-primary font-medium">
                            Inicia Sesión
                        </Link>
                    </p>
                </div>
            </div>

            <style>{`
                .aspirant-theme {
                    background: 
                      linear-gradient(135deg, rgba(248, 250, 252, 0.94) 0%, rgba(241, 245, 249, 0.96) 100%),
                      url('../../../assets/background.png') center/cover no-repeat;
                }
                .aspirant-theme::before {
                    background: 
                      radial-gradient(at 15% 15%, rgba(203, 213, 225, 0.4) 0px, transparent 55%),
                      radial-gradient(at 85% 85%, rgba(226, 232, 240, 0.5) 0px, transparent 55%);
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
                .uppercase { text-transform: uppercase; }
            `}</style>
        </div>
    );
}
