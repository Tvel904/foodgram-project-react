from api.serializers import SubscribeSerializer
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import Subscribe, User
from users.serializers import CustomUserSerializer


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return (AllowAny(),)
        return super().get_permissions()

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        if request.method == 'POST':
            return self.to_add(Subscribe, request.user, id)
        if request.method == 'DELETE':
            return self.to_delete(Subscribe, request.user, id)

    def to_add(self, model, user, pk):
        author = User.objects.get(id=pk)
        if model.objects.filter(subscriber=user, author__id=pk).exists():
            return Response({'errors': 'Вы уже подписаны на этого автора!'},
                            status=status.HTTP_400_BAD_REQUEST)
        if self.request.user == author:
            return Response({'errors': 'Вы не можете подписаться на себя!'},
                            status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(subscriber=user, author=author)
        serializer = SubscribeSerializer(
            author, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def to_delete(self, model, user, pk):
        subscription = model.objects.filter(subscriber=user, author__id=pk)
        if not subscription.exists():
            return Response(
                {'errors': 'Вы и так не подписаны на этого автора!'},
                status=status.HTTP_400_BAD_REQUEST)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(subscribers__subscriber=user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscribeSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
