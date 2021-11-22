from rest_framework import serializers
from mirumee_webapp.models import RocketCore, User


class RocketCoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RocketCore
        fields = ['url','core_id', 'reuse_count', 'total_payload_mass']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'favorite_core']
