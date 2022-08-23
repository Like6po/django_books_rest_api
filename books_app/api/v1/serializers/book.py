from rest_framework import serializers, status

from api.v1.models.author import Author
from api.v1.models.book import Book
from api.v1.serializers.author import AuthorSerializer


class BooksSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    name = serializers.CharField(max_length=256)
    publish_date = serializers.DateField("%d.%m.%Y")
    archived = serializers.BooleanField()
    authors = AuthorSerializer(many=True, required=False, read_only=True)

    def create(self, validated_data):
        new_book = Book.objects.create(name=validated_data.get("name"),
                                       publish_date=validated_data.get("publish_date"),
                                       archived=validated_data.get("archived"))
        new_book.authors.add(self.context.get("user", None))
        return new_book


class BookCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    author = AuthorSerializer(required=False, read_only=True)
    text = serializers.CharField(max_length=4096)


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    name = serializers.CharField(max_length=256, required=False)
    publish_date = serializers.DateField("%d.%m.%Y", required=False)
    archived = serializers.BooleanField(required=False)
    authors = AuthorSerializer(many=True, required=False, read_only=True)
    comment_set = BookCommentSerializer(many=True, required=False, read_only=True)


class BookUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    name = serializers.CharField(max_length=256, required=False)
    publish_date = serializers.DateField("%d.%m.%Y", required=False)
    archived = serializers.BooleanField(required=False)
    authors = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Author.objects.all())

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Empty data", code=status.HTTP_400_BAD_REQUEST)
        return data

    def update(self, instance: Book, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.publish_date = validated_data.get("publish_date", instance.publish_date)
        instance.archived = validated_data.get("archived", instance.archived)
        instance.authors.set(validated_data.get("authors", instance.authors.all()))
        instance.save()
        return instance
