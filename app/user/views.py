"""
Views for the user API
"""
from typing import Optional

from core.models import (
    BillingAddress,
    ShippingAddress,
    User,
    JwtToken,
    ROLE_ADMIN,
)
from core.permissions import BackofficePermission, ReadOnlyDevBackofficePermission
from django.contrib.auth import authenticate
from django.db import transaction
from django.http import Http404
from rest_framework import permissions, viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView

from .authenticate import JWTAuthenticationSafe
from .functions import generate_auth_token, get_object_for_login
from .serializers import (
    UserSerializer,
    BillingAddressSerializer,
    ShippingAddressSerializer,
    InputSignupSerializer,
    UserUpdateSerializer,
    ListBackofficeUserSerializer,
    BackOfficeUserSerializer,
)


# from rest_framework.exceptions import ValidationError


##############################################################
#
#
# APP Users
#
#
##############################################################
class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Create a new user in the system."""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    # Encrypt password
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

    def create(self, request, *args, **kwargs):
        dict_data = request.data.copy()

        with transaction.atomic():
            serializer, headers = self._basic_operations(dict_data)
            email = serializer.data.get("email")
            user = User.objects.get(email=email)

        return Response(
            get_object_for_login(user, request, is_user_create=True),
            status=HTTP_201_CREATED,
            headers=headers,
        )

    def _basic_operations(self, dict_data: dict) -> [UserSerializer, dict]:
        serializer = self.get_serializer(data=dict_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return serializer, headers


class Userviewset(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Update user
    """

    authentication_classes = (JWTAuthenticationSafe,)
    serializer_class = UserUpdateSerializer
    permissions_classes = permissions.IsAuthenticated
    queryset = User.objects.all()

    def get_object(self):
        try:
            if self.kwargs["pk"] != str(self.request.user.id):
                raise Http404
            return self.request.user
        except User.DoesNotExist:
            raise Http404

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer, user = self._basic_operations(kwargs)

        token = generate_auth_token(self.request.user, self.request)
        # user signature no more correct after changing email,
        # re-fetch a token with new user data
        newdict = {"token": token}
        newdict.update(serializer.data)

        return Response(newdict)

    def _basic_operations(self, kwargs: dict) -> [UserUpdateSerializer, User]:
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=self.request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return serializer, instance


class UserChangePassword(APIView):
    """
    patch:
    Change user password in settings.
    Send as PATCH parameters: "old_password" and "new_password"
    """

    authentication_classes = (JWTAuthenticationSafe,)
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, format=None):
        user = request.user
        err = self._check_missing_params(user, request.data)
        if err:
            return err

        # Change password
        user.set_password(request.data["new_password"])
        user.save()

        return Response(
            {"status": "success", "message": "Your password was successfully changed."},
            status=HTTP_200_OK,
        )

    @staticmethod
    def _check_missing_params(user: User, dict_data: dict) -> Optional[Response]:
        dict_missing_params = {}
        if "old_password" not in dict_data:
            dict_missing_params["old_password"] = ["This field is required"]
        else:
            # authenticate user
            user = authenticate(email=user.email, password=dict_data["old_password"])
            if user is None:
                dict_missing_params["old_password"] = [
                    "Your old password is not valid."
                ]

        if "new_password" not in dict_data:
            dict_missing_params["new_password"] = ["This field is required"]

        if len(dict_missing_params) > 0:
            return Response(dict_missing_params, status=HTTP_400_BAD_REQUEST)
        return


# class CreateTokenView(ObtainAuthToken):
#     """Create a new auth token for user."""
#
#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# class ManageUserView(generics.RetrieveUpdateAPIView):
#     """Manage the authenticated user."""
#
#     serializer_class = UserSerializer
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         """Retrieve the authenticated user"""
#         return self.request.user


class BillingAddressViewset(viewsets.ModelViewSet):
    """
    API to Manage Billing address
    """

    serializer_class = BillingAddressSerializer
    authentication_classes = (JWTAuthenticationSafe,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return BillingAddress.objects.filter(customer=user)


class ShippingAddressViewset(viewsets.ModelViewSet):
    """
    API to Manage Billing address
    """

    serializer_class = ShippingAddressSerializer
    authentication_classes = (JWTAuthenticationSafe,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return ShippingAddress.objects.filter(customer=user)


class SignUpView(APIView):
    """
    Sign up to the app
    """

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = InputSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        with transaction.atomic():
            user = User.objects.create(
                email=validated_data.get("email"),
                first_name=validated_data.get("first_name"),
                last_name=validated_data.get("last_name"),
                phone_prefix=validated_data.get("phone_prefix"),
                phone_number=validated_data.get("phone_number"),
                birth_date=validated_data.get("birth_date"),
            )
            user.set_password(validated_data["password"])
            user.save()

        return Response(
            get_object_for_login(user, request),
            status=HTTP_201_CREATED,
        )


class AuthLoginView(APIView):
    """
    Login to the App
    send Email and password :
        - user connects
        -
    """

    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        email = data.get("email", "").lower().replace(" ", "")
        password = data.get("password", "")
        user = authenticate(email=email, password=password)
        # Generate token and add it to the response object
        if user is not None:
            return Response(get_object_for_login(user, request), status=HTTP_200_OK)

        return Response(
            {
                "status": "unauthorized",
                "message": "Username/password combination invalid.",
            },
            status=HTTP_401_UNAUTHORIZED,
        )


class AuthLogoutview(APIView):
    """
    View to logout from the app
    """

    authentication_classes = (JWTAuthenticationSafe,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        jwt_token = JwtToken.objects.get(
            user=self.request.user,
            is_logged_out=False,
            token_access=token["access"],
            token_refresh=token["refresh"],
        )
        jwt_token.is_logged_out = True
        jwt_token.save()

        return Response({"msg": "Successfully Logged out"}, status=HTTP_200_OK)


##############################################################
#
#
# Backoffice Users
#
#
##############################################################


class BackofficeUserViewset(viewsets.ModelViewSet):
    authentication_classes = JWTAuthenticationSafe
    permission_classes = (BackofficePermission, ReadOnlyDevBackofficePermission)

    def get_serializer_class(self):
        if self.action == "list":
            return ListBackofficeUserSerializer
        else:
            return BackOfficeUserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.bimedoc_role != ROLE_ADMIN:
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        password = serializer.data["password"]
        user = serializer.save()
        user.set_password(password)
        user.save()
        return password

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data.update({"password": password})
        return Response(data, status=HTTP_201_CREATED, headers=headers)
