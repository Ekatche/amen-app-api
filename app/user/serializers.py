"""
serializer for the user api view
"""

from core.models import BillingAddress, ShippingAddress, User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects"""

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "phone_prefix",
            "phone_number",
            "gender",
            "password",
            "first_name",
            "last_name",
            "birth_date",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        read_only_fields = ("date_created", "date_modified")

    def validate_phone_prefix(self, value):
        if not value.startswith("+"):
            raise ValidationError({"errors": ["phone_prefix must start with +"]})

        if value:
            return value.replace(" ", "").replace(".", "").replace("\xa0", "")

        return value

    def validate_phone_number(self, value):
        if value:
            return value.replace(" ", "").replace(".", "").replace("\xa0", "")

        return value

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        validated_data["email"] = validated_data["email"].lower().strip()
        return get_user_model().objects.create_user(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_prefix",
            "phone_number",
            "gender",
            "first_name",
            "last_name",
            "birth_date",
        )
        read_only_fields = ("date_created", "date_modified")

        def update(self, instance, validated_data):
            user = super().update(instance, validated_data)
            return user

        def validate_email(self, email):
            return email.lower().strip()

        def validate_phone_prefix(self, value):
            if not value.startswith("+"):
                raise ValidationError({"errors": ["phone_prefix must start with +"]})

            if value:
                return value.replace(" ", "").replace(".", "")

            return value

        def validate_phone_number(self, value):
            if value:
                return value.replace(" ", "").replace(".", "")

            return value


class AuthLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=50)


class BillingAddressSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = BillingAddress
        fields = [
            "id",
            "customer",
            "building_number",
            "street",
            "city",
            "postcode",
        ]


class ShippingAddressSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "customer",
            "building_number",
            "street",
            "city",
            "postcode",
        ]


class InputSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False)
    password = serializers.CharField(
        style={"input_type": "password"},
        allow_null=False,
        max_length=128,
        write_only=True,
    )
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    first_name = serializers.CharField(allow_null=False, max_length=100)
    last_name = serializers.CharField(allow_null=False, max_length=100)
    gender = serializers.CharField(allow_null=False)
    phone_prefix = serializers.CharField(allow_null=False, max_length=10, required=True)
    phone_number = serializers.CharField(allow_null=False, max_length=30, required=True)
    birth_date = serializers.DateTimeField(allow_null=False, required=True)

    def validate(self, attrs):
        attrs["phone_prefix"] = attrs["phone_prefix"].replace(" ", "").replace(".", "")
        attrs["phone_number"] = attrs["phone_number"].replace(" ", "").replace(".", "")
        attrs["email"] = attrs.get("email").lower()

        try:
            User.objects.get(email=attrs["email"])
            raise ValidationError({"errors": ["email already in use"]})
        except User.DoesNotExist:
            pass

        if attrs["password2"] != attrs["password"]:
            raise serializers.ValidationError({"password": "Password must match"})
        elif len(attrs["password"]) < 5:
            raise serializers.ValidationError(
                {"password": "Password must be minimum 5 caracters"}
            )

        attrs["gender"] = attrs["gender"].lower()
        return attrs


# # #####################################################
#
# BackOffice serializers
#
# # ######################################################


class ListBackofficeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_prefix",
            "phone_number",
            "gender",
            "first_name",
            "last_name",
            "birth_date",
        )
        read_only_fields = fields

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset


class BackOfficeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_prefix",
            "phone_number",
            "gender",
            "first_name",
            "last_name",
            "birth_date",
        )
        read_only_fields = ("date_created", "date_modified")

        @staticmethod
        def setup_eager_loading(queryset):
            return queryset

        def validate_email(self, email):
            return email.lower().strip()

        def validate_phone_prefix(self, value):
            if not value.startswith("+"):
                raise ValidationError({"errors": ["phone_prefix must start with +"]})

            if value:
                return value.replace(" ", "").replace(".", "")

            return value

        def validate_phone_number(self, value):
            if value:
                return value.replace(" ", "").replace(".", "")

            return value

        def create(self, validated_data):
            instance = super().create(validated_data)
            return instance

        def update(self, instance, validated_data):
            return super().update(instance, validated_data)
