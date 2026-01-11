from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "username"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure 'username' is not strictly required if 'email' provides the credential
        self.fields["username"] = serializers.CharField(required=False)
        self.fields["email"] = serializers.CharField(required=False)

    def validate(self, attrs):
        login_input = attrs.get("username") or attrs.get("email")

        if not login_input:
             raise serializers.ValidationError("Must provide 'username' or 'email'.")

        if login_input:
            user = User.objects.filter(
                Q(username=login_input) | Q(email=login_input)
            ).first()

            if user:
                # We resolved the user. SimpleJWT expects the credential in attrs[self.username_field].
                # self.username_field is 'username'.
                # Django's authenticate() will receive this value as the first argument (username).
                # Since User.USERNAME_FIELD is 'email', Django's default backend expects this value to be the email.
                attrs["username"] = user.email
                
                # Cleanup 'email' input if present to avoid confusion, though not strictly necessary
                if "email" in attrs:
                    del attrs["email"]
        
        return super().validate(attrs)