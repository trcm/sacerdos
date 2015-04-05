from rest_framework import serializers
from wallfly.models import Property, Agent, WFUser


class PropertySerializer(serializers.ModelSerializer):
    """
    PropertySerializer
    Simple json serializer for retrieving and creating the property objects
    """

    class Meta:
        model = Property
        depth = 3


class AgentSerializer(serializers.ModelSerializer):

    properties = serializers.PrimaryKeyRelatedField(many=True,
                                                    queryset=Property.objects.all())
    
    class Meta:
        model = Agent
        fields = ('properties', )
        depth = 3

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = WFUser
        depth = 3
