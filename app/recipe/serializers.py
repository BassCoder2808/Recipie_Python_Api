from rest_framework import serializers

from core.models import Tag


class TagSerializers(serializers.ModelSerializer):
    """Serializers for our Tag model"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
