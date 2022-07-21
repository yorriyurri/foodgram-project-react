from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Subscribe, User
from .serializers import SubscribeSerializer, UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_list_or_404(Subscribe, user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        subscribe = Subscribe.objects.create(
            user=request.user, author=user)
        serializer = SubscribeSerializer(subscribe,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        author_id = self.kwargs['id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe, user__id=user_id, author=author_id)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
