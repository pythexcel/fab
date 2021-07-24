from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

class CustomAuthentication(ModelBackend):
    def authenticate(self, email=None, phone=None, password=None,**kwargs):
        User = get_user_model()
        try:
            if email is not None:
                user = User.objects.get(email=email) 
            else:
                user = User.objects.get(phone=phone)
            pwd_valid = user.check_password(password)
            if pwd_valid:            
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None