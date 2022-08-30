from rest_framework import serializers

from api.v1.models.book.book_favorite import BookFavorite
from api.v1.serializers.book.book import BooksSerializer


class FavoriteBookIdSerializer(serializers.Serializer):
    book = serializers.IntegerField()


class FavoriteBooksSerializer(serializers.ModelSerializer):
    book = BooksSerializer(read_only=True)

    class Meta:
        model = BookFavorite
        fields = ("created_at", "book")
        read_only_fields = ('id', "created_at")

    def create(self, validated_data):
        favorite_book = BookFavorite.objects.create(book=self.context.get("book"),
                                                    author=self.context.get("author"))
        return favorite_book
