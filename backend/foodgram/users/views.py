from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
#from django.db.models.aggregates import Case, When
from django.db.models import Case, CharField, Value, When
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from djoser.utils import logout_user
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Subscribe
from .permissions import CustomPermission
from .serializers import UserSerializer

User = get_user_model()

#admin = User.object.get(id=1)

#subs = Subscribe.objects.all().filter(subscriber=admin)

#users = User.objects.all().annotate(is_subscribed=Case(When(id__in=subs, then=Value('true')), output_field=CharField(), default=Value('false')))


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    permission_classes = (CustomPermission,)# IsSuperuser | IsAdmin,)

    def get_queryset(self):
        user = self.request.user
        subs = Subscribe.objects.all().filter(subscriber=user.pk)
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_subscribed=Case(When(id__in=subs, then=Value('true')),
                               output_field=CharField(),
                               default=Value('false')
                               )
        )
        return queryset

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['get'],
            url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['post'],
            url_path='set_password')
    def set_password(self, request):
        data = {}
        for field in ['new_password', 'current_password']:
            if field not in request.data:
                data[field] = 'is required!'
                return Response(data)
        if request.user.check_password(request.data['current_password']):
            try:
                validate_password(request.data['new_password'], request.user)
            except Exception as error:
                return Response(data={'errors': ' '.join(error)})
            request.user.set_password(request.data['new_password'])
            request.user.save()
            logout_user(request)
            return Response(data={'message': "Success!"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response(data={'errors': 'wrong password'})
