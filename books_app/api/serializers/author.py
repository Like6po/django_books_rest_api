from rest_framework import serializers

from api.models.author import Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'second_name']

