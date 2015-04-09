from rest_framework import serializers
from django.contrib.auth.models import User
from wallfly.models import Property, Agent, WFUser, Issue

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

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


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = WFUser
        depth = 3
