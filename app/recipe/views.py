from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient

from recipe import serializers

# Create your views here.


class BaseRecipeAtrrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base view set for our Recipe API"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAtrrViewSet):
    """To manage Tag model views"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializers


class IngredientViewSet(BaseRecipeAtrrViewSet):
    """To manage Ingredient views"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
