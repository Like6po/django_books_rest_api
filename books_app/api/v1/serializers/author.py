from rest_framework import serializers


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=32)
    second_name = serializers.CharField(max_length=32)
