"""
Author: Nitish Patel
Date: 05-01-2022
"""

import datetime

from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from registration.models import user
from registration.serializers import UserLimitedSerializer
from registration.views import create_hashed_password
from registration import utils
from django.db import transaction
from django.utils.timezone import make_aware
import os
class UserViewSet(viewsets.ViewSet):

    @action(methods=['GET'], url_path=r'(?P<username>[-\w@.]+)/ValidateForgotPassword/(?P<authentication_code>[^\.]+)',
            detail=False)
    def validate_forgot_password(self, request, username, authentication_code):
        """
        Validate a code sent in email with the code stored in database see if they are same.
        If same, the give response that password reset link is valid
        """
        success = 0
        data = None
        try:
            print(username)
            current_user = user.objects.get(username=username)
        except user.DoesNotExist:
            message = "Link is not valid."
        else:

            if current_user.forgot_password_is_active is False:
                message = 'Forgot Password is not active. Please request forgot password again.'
            else:
                fd = current_user.forgot_pass_time
                aware_datetime = make_aware(datetime.datetime.now())

                if str(fd.date()) > str(datetime.datetime.now().date()):
                    message = 'Forgot Password link has expired'
                    current_user.forgot_password_is_active = False
                    current_user.save()
                else:
                    if not current_user.forgot_pass_code == authentication_code:
                        message = f'Forgot password authentication code is Invalid.'
                    else:
                        message = 'Forgot password authentication code is valid.'
                        success = 1
                        data = UserLimitedSerializer(current_user).data

                        pass_reset_secret_key = utils.create_random_code(length=16)
                        current_user.forgot_password_reset_secret_key = pass_reset_secret_key
                        current_user.forgot_password_reset_secret_time = datetime.datetime.now()
                        current_user.save()

                        server_address = f"{request.scheme}://{request.get_host()}"

                        # Hardcoded API called by self.reset_password() function
                        data[
                            'reset_password_link'] = f"{server_address}/users/User/{username}/ResetPassword/{pass_reset_secret_key}/"
                        # return HttpResponseRedirect(
                        #     f'http://localhost:3000/registration/forgotpassword?reset_password_key={pass_reset_secret_key}&email={username}')
                        return HttpResponseRedirect(f'{os.environ.get("FRONTEND_URL")}/registration/forgotpassword?reset_password_link={data["reset_password_link"]}')

        return HttpResponse(message)
        # return Response({'message': message,
        #                  'data': data,
        #                  'success': success})



    @transaction.atomic
    @action(methods=['PUT'], url_path=r'(?P<username>[-\w@.]+)/ResetPassword/(?P<secret_key>[^\.]+)',
            detail=False)
    def reset_password(self, request, username, secret_key):
        """
        First validate if the secret code is valid. If valid, then use this PUT request to change
        the password.
        """

        data = None
        success = 0

        try:
            current_user = user.objects.get(username=username)
        except user.DoesNotExist:
            message = "Link is not valid."
        else:
            new_password = request.data.get('password')

            if new_password:
                cfd = current_user.forgot_password_reset_secret_time
                aware_time = make_aware(datetime.datetime.now() )

                if current_user.forgot_password_reset_secret_key != secret_key:
                    # Match the secret key.
                    message = "Invalid Code"

                elif (aware_time - cfd) > datetime.timedelta(minutes=5):
                    message = 'Page Expired'

                    # Invalidate secret key when time is greater than 5 minutes and API is hit
                    current_user.forgot_password_reset_secret_key = None
                    current_user.forgot_password_reset_secret_time = None
                    current_user.save()
                else:

                    current_user.password = create_hashed_password(new_password)
                    current_user.forgot_password_is_active = False
                    current_user.forgot_password_reset_secret_key = None
                    current_user.forgot_password_reset_secret_time = None
                    current_user.last_password_change = datetime.datetime.now()
                    current_user.save()

                    data = UserLimitedSerializer(current_user).data
                    message = 'Password Changed Successfully'
                    success = 1
            else:
                message = 'Password not provided'

        return Response({'message': message,
                         'data': data,
                         'success': success})
