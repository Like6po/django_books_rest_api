import bcrypt
from rest_framework import serializers

from api.models.author import Author
from api.models.book import Book
from api.models.comment import Comment
from api.token import RefreshJWToken


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'second_name']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'publish_date', 'archived', 'authors']


class BookManualSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    name = serializers.CharField(max_length=256)
    publish_date = serializers.DateField("%d.%m.%Y")
    archived = serializers.BooleanField()
    authors = AuthorSerializer(many=True, required=False)

    def create(self, validated_data):
        new_book = Book.objects.create(name=validated_data.get("name"),
                                       publish_date=validated_data.get("publish_date"),
                                       archived=validated_data.get("archived"))
        return new_book

    def update(self, instance: Book, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.publish_date = validated_data.get("publish_date", instance.publish_date)
        instance.archived = validated_data.get("archived", instance.archived)
        instance.save()
        return instance


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'book', 'text']


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
        token = RefreshJWToken(data["refresh_token"])
        if not token.verify():
            return serializers.ValidationError("Refresh token invalid")
        self.token = token
        return data


class AuthorInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
