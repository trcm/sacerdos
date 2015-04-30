from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wallfly.models import *
from wallfly.permissions import IsRelatedToUser, IsOwnUser
from wallfly.serializers import PropertySerializer, AgentSerializer, UserSerializer, IssueSerializer, TenantSerializer, WFUserSerializer

from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.core import serializers


# Define AGENT, OWNER and TENANT to a user level
AGENT  = 1
OWNER  = 2
TENANT = 3


# Default view, redirect the user to the base html file
def home(request):
    return render(request, 'base.djhtml')


# Converts a property status into a string for the css class in the template
def convertStatusToString(status):
    print status
    print type(status)
    if status == 1:
        return "one"
    elif status == 2:
        return "two"
    elif status == 3:
        return "three"


class AuthView(APIView):
    """
    AuthView
   
    Controller to access the user model.  In reality this code is just used to set the username in the Angular controllers.
 
    Methods:
    get(self, request, format=None):
    Returns the username and auth token of the user 
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    def get(self, request, format=None):
        
        userToken = Token.objects.get(key=request.auth)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),
            'id'  : userToken.user_id
        }
        return Response(content)

class PropertyDetail(APIView):
    
    """
    PropertyDetail
    The property detail view is used to return the details for a particular propety

    
    Methods:
    get(self, request, pk, format=None):
    Returns a JSON object containing the details for a property
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsRelatedToUser, )

    def get(self, request, pk, format=None):
        print pk
        ret = {}
        try:
            # get and serialize the property
            prop = Property.objects.get(id=pk)
            ps = PropertySerializer(prop)
            self.check_object_permissions(request, prop)
            # make a mutable copy and add the status string to the copy
            ret = ps.data.copy()
            ret['status_string'] = convertStatusToString(ret['status'])

            # get the tenant information
            ten = Tenant.objects.get(property_id=prop)
            tenSerialized = TenantSerializer(ten)
            ret['tenant'] = tenSerialized.data
            return Response(ret, status=200)
        except Property.DoesNotExist:
            # The property doesn't exist, raise a 404 call
            raise Http404
        except Tenant.DoesNotExist:
            # there's no tenants in the property, just return the data
            ret['tenant'] = 'NA'
            return Response(ret, status=200)


class PropertyView(APIView):
    
    """
    PropertyView - returns all the propets for a particular user
    # TODO - currently this is hardcoded to retrieve a particular users properties,
      in this case it is hardcoded because we were just working on the agent view,
      in the future this will work dynamically   
 
    Methods:
    get(self, request, format=None)
    Returns a list of properties as a JSON object
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        ## hardcoded agent id BAD BAD
        agent = WFUser.objects.get(id=1)
        print agent
        print agent.agent_id

        #get and serialize the list of properties for this agent
        properties = Property.objects.filter(agent_id=agent.agent_id)
        serializer = PropertySerializer(properties, many=True)
            
        return Response(serializer.data)


### NOT USED CURRENTLY
class AgentView(APIView):
    
    """
    The agent view will be used in the future for more agent specific tasks.
 
    Methods:
    get(self,request, pk, format=None)
    CUrrently not used, all this does is return a list of properties as a JSON object
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        print pk
        try:
            # get the agent and their properties
            agent = Agent.objects.get(id=pk)
            props = Property.objects.filter(agent_id=agent)
            serial = PropertySerializer(props, many=True)
            return Response(serial.data)

        except Agent.DoesNotExist:
            raise Http404


class UserDetail(APIView):
    """
    UserDetail
    This view will be used in the future for actually gettign all the users information.
    The three levels of user level will return three different types of data.

    Methods:
    get(self, request, pk, format)
    
    The Agent view will return a list of their managed properties.
    The Tenant view will return just their single property.
    The Owner view will return a view much like that of the agent view but with less detail

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnUser, )

    def get(self, request, pk, format=None):

        try:
            # try grabbing and serializing the WFUser object for the user
            print 'grabbing user'
            u = WFUser.objects.get(id=pk)
            print u
            self.check_object_permissions(request, u)

            us = WFUserSerializer(u)
            
            if u.user_level == AGENT:
                print 'agent'
                # grab all the properties for the user
                props = Property.objects.filter(agent_id=u.agent_id)
                for p in props:
                    p.status_string = convertStatusToString(p.status)
                ps = PropertySerializer(props, many=True)

                for p in ps.data:
                    # insert the status strigns for the properties into the JSON object
                    p['status_string'] = convertStatusToString(p['status'])
                    prop = Property.objects.get(property_id=p['property_id'])

                    #grab, serialize and insert the issues for the property into the JSON object
                    issues = Issue.objects.filter(property_id=prop)
                    issuesSerialized = IssueSerializer(issues, many=True)
                    p['issues'] = issuesSerialized.data
                    print p['property_id']

                
                ret = us.data
                ret['props'] = ps.data
                return Response(ret)

            elif u.user_level == OWNER:
                # user is an owner, simply grab their properties
                # This may include the issues at some point if the grup decides the owner
                # should have this functionality
                props = Property.objects.filter(owner_id=u.owner_id)
                ps = PropertySerializer(props, many=True)
                ret = us.data
                ret['props'] = ps.data
                return Response(ret)

            elif u.user_level == TENANT:
                # user is a tenant, grab their property
                # this  will also include issues
                try:
                    prop = u.tenant_id.property_id
                    prop.status_string = convertStatusToString(prop.status)
                    ps = PropertySerializer(prop)
                    ret = us.data
                    ret['prop'] = ps.data
                    ret['prop']['status_string'] = convertStatusToString(prop.status)
                    return Response(ret)
                except Exception as e:
                    print e
                    raise Http404

        # User doesn't exist raise 404
        except WFUser.DoesNotExist:
            raise Http404


class IssueList(APIView):
    
    """
    IssueList
    Returns a list of issues for a specific property 

    Methods:
    get(self, request, pk, format=None)
    Grab all the properties and the issues and return them
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            # try and get the property
            prop = Property.objects.get(id=pk)
            # filter the issues in the database for the specific property
            issues = Issue.objects.filter(property_id=prop)

            # Serialzie and return the issues
            issueSerialized = IssueSerializer(issues, many=True)
            return Response(issueSerialized.data, status=200)

        except Property.DoesNotExist:
            raise Http404


class IssueDetail(APIView):
    
    """
    IssueDetail
    This view controls the varisous methods associated with issues
    
    Methods:
    severityString(severity) - Accepts a number from 1-3 representing the severity of an issue,
    returns the corresponding error string.

    get(self, request,pk, format=None) - Will return all the details for an issue, not yet implemented.
    post(self, request, pk, format=None) - Create a new issue for a particular property
    put(self, request, pk, format=None) - Update the details of an Issue
    delete(self, request, pk, format=None) - Delete an issue from the database
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def severityString(severity):
        # Return a string based on the severity of the issue.
        if severity is 1:
            return "Mild"
        elif severity is 2:
            return "Moderate"
        elif severity is 3:
            return "Severe"
    
    def get(self, request, pk, format=None):
        # This will return all the details of a particular issue.  Not yet impletementd
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

        try:
            # grab the property
            prop = Property.objects.get(id=pk)
            request.data['property_id'] = prop.id
            # serialize the data from the user as a new Issue
            issue = IssueSerializer(data=request.data)
            if issue.is_valid():

                issue.save()
                # update the severity of the status of the property
                # TODO refactor into different method
                issues = Issue.objects.filter(property_id=prop)
                highest = 0
                for i in issues:
                    print "severity", i.severity
                    if i.severity > highest and i.resolved < 1:
                       print highest
                       highest = i.severity
                prop.status = highest
                print highest
                prop.save()

                return Response(issue.data)
            else:
                return Response(issue.errors)

        except Property.DoesNotExist:
            # Raise 404 if the property doesn't exist
            raise Http404

        except Exception as e:
            # catch generic exception
            print e

        # Something went really wrong, return a 400
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # update an Issue, at the moment this is just used to resolve the issue but
    # it could be used to change any part of the issue
    def put(self, request, pk, format=None):
        # grab the issue
        try:
            issue = Issue.objects.get(id=pk)
        except Issue.DoesNotExit:
            raise Http404

        # create a new object using the existing data and the data from the request
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # update the status of the property
            prop = issue.property_id
            issues = Issue.objects.filter(property_id=prop)
            highest = 1
            for i in issues:
                print "severity", i.severity
                if i.severity > highest and i.resolved < 1:
                    highest = i.severity
            prop.status = highest
            print highest
            prop.save()
            
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete an issue from the database
    def delete(self, request, pk, format=None):
        try:
            # Try grabbing and deleting the object
            issue = Issue.objects.get(id=pk)
            print issue
            prop = issue.property_id
            print prop
            issue.delete()

            # Update the severity status of the property
            issues = Issue.objects.filter(property_id=prop)
            highest = 1
            for i in issues:
                print "severity", i.severity
                if i.severity > highest:
                    highest = i.severity
            prop.status = highest
            print highest
            prop.save()

            # Nothing to return
            return Response(status=204)

        except Issue.DoesNotExist:
            raise Http404
