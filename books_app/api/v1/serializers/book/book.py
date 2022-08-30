from rest_framework import serializers, status

from api.v1.models.book.book import Book
from api.v1.models.book.book_categories import BookCategory
from api.v1.models.user import User


class BookAuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    first_name = serializers.CharField(max_length=128)
    second_name = serializers.CharField(max_length=128)
    patronymic = serializers.CharField(max_length=128)


class BooksSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    name = serializers.CharField(max_length=256)
    publish_date = serializers.DateField("%d.%m.%Y")
    archived = serializers.BooleanField(required=False)
    authors = BookAuthorSerializer(many=True, required=False, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=BookCategory.objects.all())
    is_favorite = serializers.BooleanField(read_only=True)
    rating = serializers.FloatField(required=False, read_only=True)

    def create(self, validated_data):
        new_book = Book.objects.create(name=validated_data.get("name"),
                                       publish_date=validated_data.get("publish_date"),
                                       archived=validated_data.get("archived", False),
                                       category=validated_data.get("category"))
        if author := self.context.get("user", None):
            new_book.authors.add(author)
        return new_book


class BookCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    author = BookAuthorSerializer(required=False, read_only=True)
    text = serializers.CharField(max_length=4096)


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    name = serializers.CharField(max_length=256, required=False)
    publish_date = serializers.DateField("%d.%m.%Y", required=False)
    archived = serializers.BooleanField(required=False)
    authors = serializers.PrimaryKeyRelatedField(many=True, required=False,
                                                 queryset=User.objects.filter(role=User.ROLES.AUTHOR.value))
    category = serializers.PrimaryKeyRelatedField(queryset=BookCategory.objects.all(), required=False)
    comment_set = BookCommentSerializer(many=True, required=False, read_only=True)
    is_favorite = serializers.BooleanField(read_only=True)
    rating = serializers.FloatField(required=False, read_only=True)

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Empty data", code=status.HTTP_400_BAD_REQUEST)
        return data

    def update(self, instance: Book, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.publish_date = validated_data.get("publish_date", instance.publish_date)
        instance.archived = validated_data.get("archived", instance.archived)
        instance.authors.set(validated_data.get("authors", instance.authors.all()))
        instance.category = validated_data.get("category", instance.category)
        instance.save()
        return instance
