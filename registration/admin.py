from django.contrib import admin
from . models import *

# Register your models here.

# admin.site.register(Role)
# admin.site.register(Group)
# admin.site.register(Permissions)
# admin.site.register(RolePermission)
admin.site.register([user,Subscribe,Plan,Role,SubscriptionOrder,RequestCall,UserAccess,Company_Users,UserAccessDb])
#admin.site.register(Role)