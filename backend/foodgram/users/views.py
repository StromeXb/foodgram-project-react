from django.contrib.auth import get_user_model
from django.db.models import Case, CharField, Value, When
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.paginator import CustomPagePaginator

from .models import Subscribe
from .permissions import CustomPermission
from .serializers import SubscribeSerializer, UserSerializer

User = get_user_model()


class UsersViewSet(UserViewSet):
    pagination_class = CustomPagePaginator
    serializer_class = UserSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        user = self.request.user
        subs = Subscribe.objects.all().filter(
            subscriber=user.pk
        ).values_list('author_id', flat=True).distinct()
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_subscribed=Case(When(id__in=subs, then=Value('true')),
                               output_field=CharField(),
                               default=Value('false')
                               )
        )
        return queryset

    @action(detail=True,
            permission_classes=[IsAuthenticated],
            methods=['GET', 'DELETE'],
            url_path='subscribe')
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, id=id)
        if user == request.user:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'errors': "You can't subscribe to yourself"}
            )
        exists = Subscribe.objects.filter(
            subscriber=request.user,
            author=user
        ).exists()
        if request.method == 'GET':
            if exists:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'errors': 'Already subscribed'}
                    )
            Subscribe.objects.create(subscriber=request.user, author=user)
            serializer = SubscribeSerializer(user)
            return Response(serializer.data)
        else:
            if not exists:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'errors': 'Not subscribed'}
                    )
            Subscribe.objects.filter(
                subscriber=request.user,
                author=user
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['get'],
            url_path='subscriptions')
    def subscriptions(self, request):
        recipes_limit = request.query_params.get('recipes_limit', 10)
        context = {'recipes_limit': recipes_limit}
        queryset = self.get_queryset().filter(is_subscribed='true')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeSerializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeSerializer(queryset, many=True, context=context)
        return Response(serializer.data)
