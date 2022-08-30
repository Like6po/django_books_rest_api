from rest_framework import serializers

from api.v1.models.book.book_rating import BookRating


class BookRatingAuthorsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    first_name = serializers.CharField(max_length=128)
    second_name = serializers.CharField(max_length=128)
    patronymic = serializers.CharField(max_length=128)


class BookRatingsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    value = serializers.IntegerField(max_value=10, min_value=1)
    author = BookRatingAuthorsSerializer(read_only=True)

    def create(self, validated_data):
        new_rating = BookRating.objects.create(value=validated_data.get("value"),
                                               book=self.context.get("book"),
                                               author=self.context.get("author"))

        return new_rating

    def update(self, instance, validated_data):
        instance.value = validated_data.get("value", instance.value)
        instance.save()
        return instance
