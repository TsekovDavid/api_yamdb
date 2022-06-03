from rest_framework import serializers
from reviews.models import Category, Genre, GenreTitle, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = GenreSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Title

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        # for genre_slug in genres:
        #     current_genre = Genre.objects.filter(slug=genre_slug['slug'])
        #     GenreTitle.objects.create(
        #         genre=current_genre, title=title)
        return title
