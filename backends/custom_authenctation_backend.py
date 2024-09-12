from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class CustomEmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Assuming the user model's username field is the email
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
