from django.contrib.auth import get_user_model
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .serializers import UserSerializer
from rest_framework import filters, status, viewsets
#from django.db.models.aggregates import Case, When
from django.db.models import CharField, Value, Case, When
from .models import Subscribe
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

User = get_user_model()

#admin = User.object.get(id=1)

#subs = Subscribe.objects.all().filter(subscriber=admin)

#users = User.objects.all().annotate(is_subscribed=Case(When(id__in=subs, then=Value('true')), output_field=CharField(), default=Value('false')))


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)# IsSuperuser | IsAdmin,)

    def get_queryset(self):
        user = self.request.user
        subs = Subscribe.objects.all().filter(subscriber=user)
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.annotate(
                is_subscribed=Case(When(id__in=subs, then=Value('true')),
                                   output_field=CharField(),
                                   default=Value('false')
                                   )
            )
        return queryset

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['get', 'patch'],
            url_path='me')
    def me(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)
