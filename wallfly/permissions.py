from rest_framework import permissions
from models import *

class IsRelatedToUser(permissions.BasePermission):

    """
    IsRelatedToUser
    Ensures that a user can only retrieve objects from the database that they have permission to view
    eg. A tenant can only see their own property, an agent can only see the propertis they manage.
    """
    def has_object_permission(self, request, view, obj):

        AGENT  = 1
        OWNER  = 2
        TENANT = 3

        tok = Token.objects.get(key=request.auth)

        wfUser = tok.user.wfuser
        
        if tok.user.is_superuser:
            return True


        if wfUser.user_level == AGENT:
            if obj.agent_id == wfUser.agent_id:
                return True
            
        elif wfUser.user_level == OWNER:
            if obj.owner_id == wfUser.owner_id:
                return True

        elif wfUser.user_level == TENANT:
            if wfUser.tenant_id.property_id == obj:
                return True
        
        
        return False

class IsOwnUser(permissions.BasePermission):

    """
    This permission will only let a user access their own details
    """
    def has_object_permission(self, request, view, obj):

        tok = Token.objects.get(key=request.auth)
        # checking permsission
        wfUser = tok.user.wfuser

        if obj == wfUser:
            return True

        return False
