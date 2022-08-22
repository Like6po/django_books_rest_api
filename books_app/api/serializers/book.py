from rest_framework import serializers

from api.models.book import Book
from api.serializers.author import AuthorSerializer


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
