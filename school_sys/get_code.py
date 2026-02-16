import os, django, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_sys.settings')
django.setup()
from users.models import User
try:
    u = User.objects.get(email="test_reset@school.com")
    print(u.mfa_code)
except:
    print("")
