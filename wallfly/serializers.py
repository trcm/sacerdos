from rest_framework import serializers
from django.contrib.auth.models import User
from wallfly.models import Property, Agent, WFUser, Issue, Tenant

class WFUserSerializer(serializers.ModelSerializer):
    """
    WFUserSerializer
    Serialzies the WFUser model to be rendered to or from JSON
    """
    class Meta:
        model = WFUser
        depth = 3

class UserSerializer(serializers.ModelSerializer):
    
    """
    UserSerializer
    Serializes the User model into a format to be rendered to or from JSON    
    """
    class Meta:
        model = User

class PropertySerializer(serializers.ModelSerializer):
    """
    PropertySerializer
    Serializes the Property model into a format to be rendered to or from JSON    
    """

    class Meta:
        model = Property
        depth = 1


class AgentSerializer(serializers.ModelSerializer):
    """
    AgentSerialzier
    Serialzies the Agent model to be rendered to or from JSON
    """
    
    properties = serializers.PrimaryKeyRelatedField(many=True,
                                                    queryset=Property.objects.all())
    
    class Meta:
        model = Agent
        fields = ('properties', )
        depth = 3


class IssueSerializer(serializers.ModelSerializer):
    """
    IssueSerializer
    Serialzies the Issue model to be rendered to or from JSON
    """
    class Meta:
        model = Issue
        

class TenantSerializer(serializers.ModelSerializer):
    """
    TenantSerializer
    Serialzies the Tentant model to be rendered to or from JSON
    """
    class Meta:
        model = Tenant
