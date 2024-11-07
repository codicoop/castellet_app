from django.contrib.auth.backends import ModelBackend

from apps.users.models import User


class IdNumberBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        dni = kwargs["username"]
        password = kwargs["password"]
        try:
            user = User.objects.get(dni__iexact=dni)
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass
