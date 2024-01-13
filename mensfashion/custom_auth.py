from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        user_model = get_user_model()
        print(f"Attempting authentication for email: {email}")
        try:
            user = user_model.objects.get(email=email)
            if user.check_password(password):
                print(f"Authentication successful for email: {email}")
                return user
            else:
                print(f"Authentication failed for email: {email}. Invalid password.")
        except user_model.DoesNotExist:
            print(f"User with email {email} does not exist.")
        return None
