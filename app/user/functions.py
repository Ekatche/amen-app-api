from core.models import JwtToken
from django.contrib.auth.models import update_last_login
from ipware import get_client_ip
from rest_framework_simplejwt.tokens import RefreshToken


# generate authentication token


def generate_auth_token(user, request):
    refresh = RefreshToken.for_user(user)
    token = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    ip_address = request.data.get("ip_address")
    user_agent = request.data.get("user_agent")

    if ip_address and user_agent:
        JwtToken.objects.create(
            user=user,
            token_access=token["access"],
            token_refresh=token["refresh"],
            ip_address=ip_address,
            user_agent=user_agent,
        )
    else:
        JwtToken.objects.create(
            user=user,
            token_access=token["access"],
            token_refresh=token["refresh"],
            ip_address=get_client_ip(request)[0],
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )
    update_last_login(None, user)

    return token


# Object to return at login
def get_object_for_login(user, request, is_user_create=False):
    token = generate_auth_token(user, request)
    return {
        "status": "success",
        "token": token,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "user": user.id,
    }
