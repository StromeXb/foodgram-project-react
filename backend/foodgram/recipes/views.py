from django.shortcuts import render
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Case, CharField, Value, When

from .models import Ingredient, Tag, Recipe, Favorite, ShoppingCart
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer

# Create your views here.


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Recipe.objects.all()

    def get_queryset(self):
        user = self.request.user
        fav = Favorite.objects.all().filter(user=user.pk)
        shop = ShoppingCart.objects.all().filter(user=user.pk)
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_favorited=Case(When(id__in=fav, then=Value('true')),
                               output_field=CharField(),
                               default=Value('false')
                               )
        ).annotate(
            is_in_shopping_cart=Case(When(id__in=shop, then=Value('true')),
                               output_field=CharField(),
                               default=Value('false')
                               )
        )
        return queryset