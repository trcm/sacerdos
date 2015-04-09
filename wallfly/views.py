from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

from wallfly.models import *
from wallfly.serializers import PropertySerializer, AgentSerializer, UserSerializer, IssueSerializer

from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

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

def convertStatusToString(status):
    if status is 1:
        return "one"
    elif status is 2:
        return "two"
    elif status is 3:
        return "three"


class AuthView(APIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    # def post(self, request, *args, **kwargs):
    #     print request.META.get( 'HTTP_AUTHORIZATION' )

    #     return Response(self.serializer_class(request.user).data)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

class PropertyDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        print pk
        try:
            prop = Property.objects.get(id=pk)
            ps = PropertySerializer(prop)

            ret = ps.data.copy()
            ret['status_string'] = convertStatusToString(ret['status'])
            
            return Response(ret, status=200)
        except:
            raise Http404
    
class PropertyView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):

        try:
            u = WFUser.objects.get(id=pk)
            us = UserSerializer(u)

            if u.user_level == AGENT:
                props = Property.objects.filter(agent_id=u.agent_id)
                for p in props:
                    p.status_string = convertStatusToString(p.status)
                ps = PropertySerializer(props, many=True)

                for p in ps.data:
                    p['status_string'] = convertStatusToString(p['status'])
                
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

class IssueDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # get all the details for an issue
    def get(self, request, pk, format=None):

        errors = {}

        # try and grab property
        try:
            print request.data
            if 'prop_id' not in request.data:
                errors['prop_error'] = "No Property id"
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            prop_id = request.data['prop_id']

        except Property.DoesNotExist:
            errors["PropertyError"] = "Property Doesn't exist"
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(prop);

    # create an issue
    def post(self, request, format=None):

        pass
