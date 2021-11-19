from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from mirumee_webapp.serializers import UserSerializer, RocketCoreSerializer
from mirumee_webapp.models import RocketCore, User
from mirumee_webapp.functions import fetch_and_save_rocket_core_data

class UserViewSet(viewsets.ModelViewSet):
    """
        Endpoint for editing/viewing users.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RocketCoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
        Endpoint for viewing Rocket Cores.
    """
    queryset = RocketCore.objects.all().order_by('-reuse_count')
    serializer_class = RocketCoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    # The retrieve and list methods below are overridden so as to detect if the database is empty, and if so, call the
    # fetch_and_save_rocket_core_data() function from functions.py
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        print(data)
        print(type(data))
        return Response(data)

    def list(self, request, *args, **kwargs):
        if not RocketCore.objects.all():
            fetch_and_save_rocket_core_data()

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        return Response(data)

