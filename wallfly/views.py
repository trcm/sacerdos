from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

from wallfly.models import *
from wallfly.serializers import PropertySerializer, AgentSerializer, UserSerializer, IssueSerializer, TenantSerializer

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
        ret = {}
        try:
            prop = Property.objects.get(id=pk)
            ps = PropertySerializer(prop)

            ret = ps.data.copy()
            ret['status_string'] = convertStatusToString(ret['status'])

            # get the tenatn information

            ten = Tenant.objects.get(property_id=prop)
            tenSerialized = TenantSerializer(ten)
            ret['tenant'] = tenSerialized.data

            return Response(ret, status=200)
        except Property.DoesNotExist:
            raise Http404
        except Tenant.DoesNotExist:
            # there's no tenant just return the data
            ret['tenant'] = 'NA'
            return Response(ret, status=200)


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


class IssueList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # get all the issues for a property
    def get(self, request, pk, format=None):
        try:
            prop = Property.objects.get(id=pk)
            issues = Issue.objects.filter(property_id=prop)
            issueSerialized = IssueSerializer(issues, many=True)
            return Response(issueSerialized.data, status=200)

        except Property.DoesNotExist:
            raise Http404



class IssueDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # get all the details for an issue
    # TODO
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

        return Response(prop)

    # create an issue, pk is the primary key id of the property of the issue
    def post(self, request, pk, format=None):
        print "new issue request"

        try:
            prop = Property.objects.get(id=pk)
            request.data['property_id'] = prop.id
            issue = IssueSerializer(data=request.data)
            if issue.is_valid():

                issue.save()

                # update the severity of the status of the property
                issues = Issue.objects.filter(property_id=prop)

                highest = 0
                for i in issues:
                    print "severity", i.severity
                    if i.severity > highest:
                       print highest
                       highest = i.severity
                prop.status = highest
                print highest
                prop.save()

                return Response(issue.data)
            else:
                return Response(issue.errors)

        except Property.DoesNotExist:
            raise Http404

        except Exception as e:
            print e

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            issue = Issue.objects.get(id=pk)
            print issue
            prop = issue.property_id
            print prop
            issue.delete()

            
            issues = Issue.objects.filter(property_id=prop)

            highest = 1
            for i in issues:
                print "severity", i.severity
                if i.severity > highest:
                    highest = i.severity
            prop.status = highest
            print highest
            prop.save()


            return Response(status=204)

        except Issue.DoesNotExist:
            raise Http404
