import base64
import json

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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

    @action(detail=True, methods=['post'])
    def designate_favorite_rocket(self, request, pk=None):
        print(request)


class RocketCoreViewSet(viewsets.ModelViewSet):
    """
        Endpoint for viewing Rocket Cores.
    """
    queryset = RocketCore.objects.all().order_by('-reuse_count')
    serializer_class = RocketCoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    # The list method below is overridden so as to detect if the database is empty, and if so, call the
    # fetch_and_save_rocket_core_data() function from functions.py
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


# Since the requirement specification for this API option is non-restful (it's stateful), a standard django HTTP view is
# used, without DRF, and the method is POST instead of PUT.
@csrf_exempt
def choose_favorite_rocket_core(request :HttpRequest):
    if request.method != "POST":
        return HttpResponseBadRequest(f"No {request.method} method for this endpoint.")

    content = request.body.decode('utf-8')

    # The API uses HTTP basic authentication and default django authentication.
    auth_header = request.META['HTTP_AUTHORIZATION']
    encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
    username = decoded_credentials[0]
    password = decoded_credentials[1]

    if authenticate(username=username, password=password):
        user = User.objects.get(username=username)
    else:
        return HttpResponseForbidden()

    if content.isnumeric():
        try:
            core = RocketCore.objects.get(id=int(content))
            user.favorite_core = core
            user.save()
            serializer = RocketCoreSerializer(core)

            return HttpResponse(json.dumps(serializer.data), status=200)
        except ObjectDoesNotExist:

            return HttpResponseBadRequest(f"No such core with id = {content}")
    elif content.isalnum():
        try:
            core = RocketCore.objects.get(core_id=content)
            user.favorite_core = core
            user.save()
            serializer = RocketCoreSerializer(core)

            return HttpResponse(json.dumps(serializer.data), status=200)
        except ObjectDoesNotExist:

            return HttpResponseBadRequest(f"No such core with core_id = {content}")
    else:
        try:
            json_content = json.loads(content)
        except json.decoder.JSONDecodeError:

            return HttpResponseBadRequest("Invalid request.Provide a JSON key-value pair of either core_id or id of the"
                                          " core or a plaintext id/core_id")

    if not any(keyword in json_content.keys() for keyword in ["id", "core_id"]):

        return HttpResponseBadRequest("Invalid request. Provide a key-value pair of either core_id or id of the core.")

    if all(keyword in json_content.keys() for keyword in ["id", "core_id"]):

        return HttpResponseBadRequest("Invalid request. Please provide only one type of identifier for the core.")

    if "id" in json_content.keys() and type(json_content["id"]) != int:

        return HttpResponseBadRequest("Invalid field type. 'id' must be an integer")

    if "core_id" in json_content.keys() and type(json_content["core_id"]) != str:

        return HttpResponseBadRequest("Invalid field type. 'core_id' must be a string.")

    if "id" in json_content.keys():
        try:
            core = RocketCore.objects.get(id=int(json_content["id"]))
            user.favorite_core = core
            user.save()
            serializer = RocketCoreSerializer(core)
            return HttpResponse(json.dumps(serializer.data), status=200)
        except ObjectDoesNotExist:

            return HttpResponseBadRequest(f"No such core with id={json_content['id']}")
    elif "core_id" in json_content.keys():
        try:
            core = RocketCore.objects.get(core_id=json_content["core_id"])
            user.favorite_core = core
            user.save()
            serializer = RocketCoreSerializer(core)
            return HttpResponse(json.dumps(serializer.data), status=200)
        except ObjectDoesNotExist:

            return HttpResponseBadRequest(f"No such core with core_id={json_content['core_id']}")


# Since the requirement specification for this API option is non-restful (it's stateful), a standard django HTTP view is
# used, without DRF, and the method is POST instead of PUT.
@csrf_exempt
def view_favorite_rocket(request :HttpRequest):
    if request.method != "GET":

        return HttpResponseBadRequest(f"No {request.method} method for this endpoint.")

    # The API uses HTTP basic authentication and default django authentication.
    auth_header = request.META['HTTP_AUTHORIZATION']
    encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
    username = decoded_credentials[0]
    password = decoded_credentials[1]

    if authenticate(username=username, password=password):
        user = User.objects.get(username=username)
        serializer = RocketCoreSerializer(user.favorite_core)
        return HttpResponse(json.dumps(serializer.data))
    else:
        return HttpResponseForbidden()
