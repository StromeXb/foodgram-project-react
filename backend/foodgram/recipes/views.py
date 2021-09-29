from django.shortcuts import render
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Case, CharField, Value, When
from rest_framework.decorators import action, api_view, permission_classes
from .models import Ingredient, Tag, Recipe, Favorite, ShoppingCart
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .paginator import CustomPagePaginator
from users.serializers import PartialRecipeSerializer
from .filters import CustomFilterBackend, CustomSearch
from .permissions import IsOwnerOrReadOnly
from rest_framework import filters
# Create your views here.


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = [CustomSearch]
    search_fields = ['^name']


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Recipe.objects.all()
    pagination_class = CustomPagePaginator
    filter_backends = [CustomFilterBackend]

    def get_queryset(self):
        user = self.request.user
        fav = Favorite.objects.all().filter(
            user=user.pk
        ).values_list('recipe_id', flat=True).distinct()
        shop = ShoppingCart.objects.all().filter(
            user=user.pk
        ).values_list('recipe_id', flat=True).distinct()
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_favorited=Case(
                When(id__in=fav, then=Value('true')),
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

    @action(detail=True,
            permission_classes=[IsAuthenticated],
            methods=['GET', 'DELETE'],
            url_path='favorite')
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        exists = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
        if request.method == 'GET':
            if exists:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'errors': 'Already in favorites'}
                    )
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = PartialRecipeSerializer(recipe)
            return Response(serializer.data)
        else:
            if not exists:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'errors': 'Not in favorites'}
                    )
            Favorite.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            permission_classes=[IsAuthenticated],
            methods=['GET', 'DELETE'],
            url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        exists = ShoppingCart.objects.filter(user=request.user, recipe=recipe).exists()
        if request.method == 'GET':
            if exists:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'errors': 'Already in shopping cart'}
                    )
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            serializer = PartialRecipeSerializer(recipe)
            return Response(serializer.data)
        else:
            if not exists:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'errors': 'Not in shopping cart'}
                    )
            ShoppingCart.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
