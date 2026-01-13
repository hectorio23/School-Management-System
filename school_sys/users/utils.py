from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random
import string

def generate_mfa_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


def send_mfa_code(user):
    """
    Genera un código MFA, lo guarda en el usuario y lo envía por email.
    """
    code = generate_mfa_code()

    user.mfa_code = code
    user.mfa_expires_at = timezone.now() + timedelta(minutes=2)
    user.save(update_fields=["mfa_code", "mfa_expires_at"])

    # Enviar por email (puedes sustituir por SMS si usas Twilio)
    send_mail(
        subject="Código MFA",
        message=f"Tu código MFA es: {code}",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return True



def verify_mfa_code(user, code_input):
    """
    Verifica si el código MFA es válido.
    """
    if not user.mfa_code or not user.mfa_expires_at:
        return False

    if timezone.now() > user.mfa_expires_at:
        user.clear_mfa()
        return False

    if str(code_input) != str(user.mfa_code):
        return False

    user.clear_mfa()
    return True
