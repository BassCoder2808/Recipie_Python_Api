from rest_framework import serializers

from core.models import Tag, Ingredient


class TagSerializers(serializers.ModelSerializer):
    """Serializers for our Tag model"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for our Ingredient model"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
