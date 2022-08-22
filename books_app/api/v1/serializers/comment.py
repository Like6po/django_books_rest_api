from rest_framework import serializers

from api.v1.models.comment import Comment


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'book', 'text']
