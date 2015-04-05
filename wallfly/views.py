from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

from wallfly.models import *
from wallfly.serializers import PropertySerializer, AgentSerializer, UserSerializer

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.core import serializers

AGENT  = 1
OWNER  = 2
TENANT = 3

def home(request):
    return render(request, 'base.djhtml')

class PropertyView(APIView):

    def get(self, request, format=None):
        ## hardcoded agent id BAD BAD
        agent = WFUser.objects.get(id=2)
        print agent
        print agent.agent_id
        properties = Property.objects.filter(agent_id=agent.agent_id)
        
        # properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        print serializer.data
        return Response(serializer.data)


class AgentView(APIView):
    
    """
    View all the properties for a particular agent
    """
    def get(self, request, pk, format=None):
        print pk
        try:
            agent = Agent.objects.get(id=pk)

            props = Property.objects.filter(agent_id=agent)
            
            serial = PropertySerializer(props, many=True)
            return Response(serial.data)

        except Agent.DoesNotExist:
            raise Http404

        
class UserDetail(APIView):

    def get(self, request,pk, format=None):

        try:
            u = WFUser.objects.get(id=pk)
            us = UserSerializer(u)

            if u.user_level == AGENT:
                props = Property.objects.filter(agent_id=u.agent_id)
                ps = PropertySerializer(props, many=True)
                ret = us.data
                ret['props'] = ps.data
                return Response(ret)
            
            elif u.user_level == OWNER:
                props = Property.objects.filter(owner_id=u.owner_id)
                ps = PropertySerializer(props, many=True)
                ret = us.data
                ret['props'] = ps.data
                return Response(ret)

            elif u.user_level == TENANT:
                prop = Property.objects.get(u.property_id)
                ps = PropertySerializer(prop)
                ret = us.data
                ret['prop'] = ps.data
                return Response(ret)
            
        except WFUser.DoesNotExist:
            raise Http404
