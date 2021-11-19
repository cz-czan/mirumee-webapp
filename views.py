from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from mirumee_webapp.serializers import UserSerializer, RocketCoreSerializer
from mirumee_webapp.models import RocketCore, User

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RocketCoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = RocketCore.objects.all().order_by('core_id')
    serializer_class = RocketCoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    # The retrieve and list methods below are overridden so as to detect if the database is empty, and if so, call the
    # fetch_and_save_rocket_core_data() function from functions.py
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(" A CURIOUS TEST")
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        print(" A CURIOUS TEST")
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

