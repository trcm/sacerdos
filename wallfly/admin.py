from django.contrib import admin
from django.contrib.auth.models import User
from wallfly.models import *

admin.site.register(Property)
admin.site.register(Owner)
admin.site.register(Agent)
admin.site.register(Tenant)
admin.site.register(Issue)
admin.site.register(Financial)
admin.site.register(WFUser)
