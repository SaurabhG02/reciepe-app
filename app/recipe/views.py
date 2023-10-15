from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the recipes for the authenticated user.
        
        Filter the queryset based on the user and order it by descending id.
        """
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-id')
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        
        return self.serializer_class
        
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the tags for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """View for manage tag APIs."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all() 
    

class IngredientViewSet(BaseRecipeAttrViewSet):
    """View for manage ingredient APIs."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

        
