from rest_framework import permissions
from models import *

class IsRelatedToUser(permissions.BasePermission):

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
