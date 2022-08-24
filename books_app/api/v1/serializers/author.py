from rest_framework import serializers, status

from api.v1.models.user import User


class AuthorBooksSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    name = serializers.CharField(max_length=256, required=False)
    publish_date = serializers.DateField("%d.%m.%Y", required=False)
    archived = serializers.BooleanField(required=False)


class AuthorsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    first_name = serializers.CharField(max_length=32)
    second_name = serializers.CharField(max_length=32)
    email = serializers.EmailField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLES.choices, read_only=True)
    book_set = AuthorBooksSerializer(many=True, read_only=True)

    def create(self, validated_data):
        author = User.objects.create(first_name=validated_data.get("first_name"),
                                     second_name=validated_data.get("second_name"),
                                     email=validated_data.get("email"),
                                     role=User.ROLES.AUTHOR.value)

        return author

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Empty data", code=status.HTTP_400_BAD_REQUEST)
        return data

    def update(self, instance: User, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.second_name = validated_data.get("second_name", instance.second_name)
        instance.save()
        return instance


class AuthorsUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    first_name = serializers.CharField(max_length=32, required=False)
    second_name = serializers.CharField(max_length=32, required=False)
    role = serializers.ChoiceField(choices=User.ROLES.choices, read_only=True)
    book_set = AuthorBooksSerializer(many=True, read_only=True)

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Empty data", code=status.HTTP_400_BAD_REQUEST)
        return data

    def update(self, instance: User, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.second_name = validated_data.get("second_name", instance.second_name)
        instance.save()
        return instance
