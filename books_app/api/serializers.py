import bcrypt
from rest_framework import serializers

from api.models import Author, Book, Comment


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'second_name']


class BookSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Book
        fields = ['id', 'name', 'publish_date', 'archived']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'book', 'text']


class LoginAuthorSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField()


class RegisterAuthorSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    second_name = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        return Author.objects.create(first_name=validated_data["first_name"],
                                     second_name=validated_data["second_name"],
                                     password_hash=bcrypt.hashpw(validated_data["password"].encode('utf-8'),
                                                                 bcrypt.gensalt()).decode("utf-8"))


class LoginAuthorSerializer(serializers.Serializer):
    author_id = serializers.IntegerField()
    password = serializers.CharField()

    def validate(self, data):
        current_author = Author.objects.get(id=data["author_id"])
        if bcrypt.checkpw(data["password"].encode('utf-8'), current_author.password_hash.encode('utf-8')):
            return {"author_id": data["author_id"], "password": data["password"]}
        raise serializers.ValidationError("Password incorrect")


class AuthorInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
