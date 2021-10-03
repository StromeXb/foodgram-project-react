from django.db.models import Case, CharField, Sum, Value, When
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.serializers import PartialRecipeSerializer
from .filters import CustomFilterBackend, CustomSearch
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .paginator import CustomPagePaginator
from .permissions import IsOwnerOrReadOnly
from .renders import BinaryFileRenderer
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = [CustomSearch]
    search_fields = ['^name']


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Recipe.objects.all()
    pagination_class = CustomPagePaginator
    filter_backends = [CustomFilterBackend]

    def get_queryset(self):
        user = self.request.user
        fav = Favorite.objects.filter(
            user=user.pk
        ).values_list('recipe_id', flat=True).distinct()
        shop = ShoppingCart.objects.filter(
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
            is_in_shopping_cart=Case(
                When(id__in=shop, then=Value('true')),
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
        exists = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()
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
        exists = ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()
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
            ShoppingCart.objects.filter(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['GET'],
            url_path='download_shopping_cart',
            renderer_classes=(BinaryFileRenderer,))
    def download_shopping_cart(self, request):
        shopping_list = ShoppingCart.objects.filter(
            user=request.user
        ).values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit__unit').annotate(
            total=Sum('recipe__recipe_content__amount')
        ).values_list(
            'recipe__ingredients__name',
            'total',
            'recipe__ingredients__measurement_unit__unit'
        )
        text = 'СПИСОК ПОКУПОК:\n'
        headers = {
            'Content-Disposition': 'attachment; filename="shopping_list.txt"'
        }
        for line in shopping_list:
            text += (str(line[0]) + ': ' + str(line[1]) +
                     ', ' + str(line[2]) + '\n')
        return Response(
            data=bytes(text.encode('utf8')),
            headers=headers,
            content_type='application/txt'
        )
