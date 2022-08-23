from rest_framework import serializers

from api.v1.models.comment import Comment
from api.v1.serializers.author import AuthorSerializer
from api.v1.serializers.book import BooksSerializer


class CommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    author = AuthorSerializer(read_only=True)
    text = serializers.CharField(max_length=4096)

    def create(self, validated_data):
        new_comment = Comment.objects.create(text=validated_data.get("text"),
                                             book=self.context.get("book"),
                                             author=self.context.get("author"))

        return new_comment


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    book = BooksSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    text = serializers.CharField(max_length=4096, read_only=True)


class CommentUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    author = AuthorSerializer(read_only=True)
    text = serializers.CharField(max_length=4096)

    def update(self, instance: Comment, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
