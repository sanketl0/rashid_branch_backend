from django.urls import include, path
from .import views
from .views import * # import List and Viewset of app from views
from rest_framework import routers
from django.contrib import admin
from django.urls import path

from . import validate_forgot_password

router = routers.SimpleRouter()
#as this url is already exist in other project so keep this url name same
router.register('postTrialRegistration', UserViewset,basename='postTrialRegistration')
router.register('postSignIn', signinViewset, basename='postSignIn')
router.register('creategroup', GroupViewset,basename='GroupViewset')
router.register('createpermissions', permissionsViewset,basename='permissionsViewset')
router.register('createrole', RoleViewset,basename='RoleViewset')
router.register('createuser', User1Viewset,basename='User1Viewset')
router.register('company_users', Company_UsersViewset,basename='Company_UsersViewset')

router.register('User', validate_forgot_password.UserViewSet, basename='ForgotPasswordUser')

urlpatterns = [
    path('', include(router.urls)),
    path('verify-user/',VerifyView.as_view()),
    #path('admin/', admin.site.urls),  
    path('getRegisteredUsers/', userList.as_view()),#Vendor and contact get api url 
    #path('userupdatebyid/<uuid:pk>/', views.userupdate, name='updatebyid'),
    path('activateuser/<str:act_code>/', views.activateuser, name='activateuser'),
    path('signin/<str:useremail>/<str:password>/', views.signin, name='signin'),
    path('email/', views.ValidateEmail, name='email'),
    path('plans/',views.PlanView.as_view()),
#     #path('verify_credentials/', verify_credentials.as_view()),#Vendor and contact get api url 
#    # path('email/<str:email>', views.verify_credentials, name='email')
#     path('login/', LoginView.as_view()),
#     path('logout/', Logout.as_view()),
#     path('groupupdate/', views.groupupdate, name='update'),
#     path('permissionupdate/', views.permissionsupdate, name='update'),
      path('permissions/', views.get_all_permissions, name='permissions'),
      path('groups/', views.get_all_groups, name='groups'),
      #url for forgot password
      # API for forgot password with forgot password code
     # path('forgotpassword/<str:pass_code>/', views.forgotpassword, name='forgotpassword'),
      # Api for forgot password without activation code
    path('forgotpassword/<str:email>/', views.forgotpassword, name='forgotpassword'),
    path('getcompanysbyuser_id/<int:id>/', views.getcompanyusersbyuser_id, name='getcompanyusersbyuser_id'),
]





