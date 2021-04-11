from django.contrib.auth import get_user_model

from accounts.models import UserTypes

User = get_user_model()


def has_permission(user=None):
    """
        Check user is `ADMIN` or `OTHERS`
    """
    has_permission = False

    if isinstance(user, User):
        print('t =', user.user_type)
        if user.user_type == UserTypes.ADMIN:
            has_permission = True

    return has_permission
