import bcrypt
from rest_framework import serializers

from api.v1.models.user import User
from api.v1.token import RefreshJWToken


class RegisterUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    first_name = serializers.CharField(max_length=128)
    patronymic = serializers.CharField(max_length=128, required=False)
    second_name = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if user:
            raise serializers.ValidationError("Email exists")
        return data

    def create(self, validated_data):
        user = User.objects.create(first_name=validated_data["first_name"],
                                   second_name=validated_data["second_name"],
                                   patronymic=validated_data.get("patronymic", None),
                                   password_hash=bcrypt.hashpw(validated_data["password"].encode('utf-8'),
                                                               bcrypt.gensalt()).decode("utf-8"),
                                   role=self.context.get("role"),
                                   email=validated_data["email"])
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        current_author = User.objects.filter(email=data["email"]).first()
        if not current_author:
            raise serializers.ValidationError("Login incorrect")
        try:
            if bcrypt.checkpw(data["password"].encode('utf-8'), current_author.password_hash.encode('utf-8')):
                return data
        except ValueError:
            raise serializers.ValidationError("Password incorrect")
        raise serializers.ValidationError("Password incorrect")


class RefreshUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        try:
            token = RefreshJWToken(data["refresh_token"])
        except ValueError:
            raise serializers.ValidationError("Refresh token invalid")
        self.token = token
        return data


class RecoveryUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError("User with this email not exists")
        self.user = user
        return data


class ChangePasswordUserSerivalizer(serializers.Serializer):
    password = serializers.CharField(min_length=6, write_only=True)
