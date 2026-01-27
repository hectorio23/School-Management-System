from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from .models import AdmissionUser

class AdmissionJWTAuthentication(JWTAuthentication):
    """
    clase de autenticacion custom para AdmissionUser.
    """
    def get_user(self, validated_token):
        try:
            user_id = validated_token["user_id"]
            user = AdmissionUser.objects.get(folio=user_id)
            if not user.is_active:
                raise AuthenticationFailed("User is inactive", code="user_inactive")
            return user
        except (AdmissionUser.DoesNotExist, KeyError):
            raise AuthenticationFailed("User not found", code="user_not_found")
