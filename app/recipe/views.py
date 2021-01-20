from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

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


class RecipeViewSet(viewsets.ModelViewSet):
    """To manage Recipe view set"""

    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Function to convert string ids to integer"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Return objects for the current user"""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tags_ids = self._params_to_ints(queryset)
            queryset = queryset.filter(tags__id__in=tags_ids)

        if ingredients:
            ingredients_tags = self._params_to_ints(queryset)
            queryset = queryset.filter(ingredients__id__in=ingredients_tags)
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Retrieve the serializer class"""

        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == ' upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Recipe"""

        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""

        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
