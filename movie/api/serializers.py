from rest_framework import serializers

from movie.models import Movie, Category, Subcategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        exclude = ['parent_category']

class CategorySerializer(serializers.Serializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validation_data):
        print(validation_data)
        return Category.objects.create(**validation_data)

    def update(self, instance, validation_data):
        instance.name = validation_data.get('name', instance.name)
        return instance


class MovieSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

