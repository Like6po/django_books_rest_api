import bcrypt
from rest_framework import serializers

from api.v1.models.author import Author
from api.v1.token import RefreshJWToken


class LoginAuthorSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField()


class RegisterAuthorSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=32)
    second_name = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6)

    def create(self, validated_data):
        return Author.objects.create(first_name=validated_data["first_name"],
                                     second_name=validated_data["second_name"],
                                     password_hash=bcrypt.hashpw(validated_data["password"].encode('utf-8'),
                                                                 bcrypt.gensalt()).decode("utf-8"))


class LoginAuthorSerializer(serializers.Serializer):
    author_id = serializers.IntegerField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            current_author = Author.objects.get(id=data["author_id"])
        except Author.DoesNotExist:
            raise serializers.ValidationError("Login incorrect")
        try:
            if bcrypt.checkpw(data["password"].encode('utf-8'), current_author.password_hash.encode('utf-8')):
                return data
        except ValueError:
            raise serializers.ValidationError("Password incorrect")
        raise serializers.ValidationError("Password incorrect")


class RefreshAuthorSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        try:
            token = RefreshJWToken(data["refresh_token"])
        except ValueError:
            return serializers.ValidationError("Refresh token invalid")
        self.token = token
        return data


class AuthorInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
