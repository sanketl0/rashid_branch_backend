from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from registration.models import user,UserAccess
from registration.views import create_hashed_password,create_random_code
from rest_framework.authtoken.models import Token
from registration.serializers import SubUserSerializer
from registration.models import Feature
from django.shortcuts import get_object_or_404
from .serializer import SubUserAccessSerializer
class SubUserView(APIView):


    def get(self,request,pk=None):
        if pk:
            instance = get_object_or_404(user,id=pk)
            serializer = SubUserAccessSerializer(instance)
            return Response(serializer.data,status=200)
        if request.user.role == 'admin':
            users = request.user.sub_users.exclude(id=request.user.id)
            print(users)
            serializer = SubUserSerializer(users,many=True)
            return Response(serializer.data,status=200)
        return Response({"message":"User is not admin"},status=401)

    @transaction.atomic
    def post(self,request):
        user_data = request.data
        count = Feature.objects.get(user_id=request.user.id).user_remaining
        print(count, 'users')
        if count <= 0:
            return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        if request.user.role == 'admin':
            role = user_data.get('role',None)
            role_detail = user_data.get('role_details',None)
            if role != 'admin' and role is not None:
                try:
                    user.objects.get(email=user_data["email"])
                    print("##########", user)
                    msg = "Email is already exist"
                    print("KKKKKKK", msg)
                    return Response({"message": msg}, status=status.HTTP_403_FORBIDDEN)
                except user.DoesNotExist:
                    try:
                        user.objects.get(mobile_no=user_data["mobile_no"])
                        print("##########", user)
                        msg = "Mobile no is already exist"
                        print("KKKKKKK", msg)
                        return Response({"message": msg}, status=status.HTTP_403_FORBIDDEN)
                    except user.DoesNotExist:
                        create_user = user(
                            name=user_data["name"],
                            mobile_no=user_data["mobile_no"],
                            email=user_data["email"],
                            password=create_hashed_password(user_data["password"]),
                            activation_code=create_random_code(),
                            role=role,
                            is_activated=True,
                            is_subscribed=user_data["is_subscribed"],
                            is_activate=user_data["is_activate"],
                            is_on_trial=True,
                            company=user_data["company"],
                            industry=user_data["industry"],
                            country=user_data["country"],
                            #   username=user_data["email"],
                            username=user_data["email"],
                            department=user_data["department"],
                            image=user_data["image"],
                            provider=user_data["provider"],
                        )
                        create_user.save()
                        token, created = Token.objects.get_or_create(user=create_user)
                        request.user.sub_users.add(create_user)
                        branches = role_detail.pop('branches')
                        subuser = UserAccess.objects.create(**role_detail)
                        subuser.user=create_user
                        subuser.branches.set(branches)
                        subuser.save()
                        return Response(status=201)
        return Response({"message":"user is not admin"},status=400)

    @transaction.atomic
    def put(self,request,pk=None):
        user_data = request.data
        print(request.user.role)
        if request.user.role == 'admin':
            role = user_data.get('role',None)
            role_detail = user_data.get('role_details',None)
            usr_obj = user.objects.get(email=user_data["email"])

            if role != 'admin' and role is not None:
                try:
                    usr = user.objects.select_for_update().get(mobile_no=user_data["mobile_no"])
                    if usr.id != usr_obj.id:
                        print("##########", user)
                        msg = "Mobile no is already exist"
                        print("KKKKKKK", msg)
                        return Response({"message": msg}, status=status.HTTP_403_FORBIDDEN)
                    else:
                        usr_obj.name = user_data["name"]
                        usr_obj.mobile_no = user_data['mobile_no']
                        usr_obj.email = user_data["email"]
                        # usr_obj.password=create_hashed_password(user_data["password"])
                        usr_obj.role = role
                        usr_obj.save()
                        subuser = UserAccess.objects.get(user=usr_obj)
                        for key, value in role_detail.items():
                            if key == "branches":
                                subuser.branches.set(value)
                            else:
                                setattr(subuser, key, value)
                        subuser.save()
                        return Response(status=201)
                except user.DoesNotExist:
                        usr_obj.name=user_data["name"]
                        usr_obj.mobile_no=user_data['mobile_no']
                        usr_obj.email=user_data["email"]
                        # usr_obj.password=create_hashed_password(user_data["password"])
                        usr_obj.role=role
                        usr_obj.save()
                        subuser = UserAccess.objects.get(user=usr_obj)
                        for key,value in role_detail.items():
                            if key == "branches":
                                subuser.branches.set(value)
                            else:
                                setattr(subuser,key,value)
                        subuser.save()
                        return Response(status=201)
        return Response({"message":"user is not admin"},status=400)