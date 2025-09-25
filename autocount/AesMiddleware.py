from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import base64
import json
import os
import traceback
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from django.db import connection, OperationalError


# AES Key should be 32 bytes (256 bits) for AES-256
AES_KEY = base64.b64decode(os.environ.get('AES_KEY'))
AES_IV = base64.b64decode(os.environ.get('AES_IV'))
strings = ["/integration", "/admin"]
def filter_strings(prefix):
    """
    Returns a list of strings that do not start with the given prefix.

    :param strings: List of strings to filter
    :param prefix: String prefix to check
    :return: List of strings that do not start with the prefix
    """
    for each in strings:

        if prefix.startswith(each):
            return False
    else:
        return True



def encrypt_aes256(data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted)


def decrypt_aes256(data: bytes) -> bytes:
    data = base64.b64decode(data)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    return unpadder.update(decrypted) + unpadder.finalize()


class AESCipherMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            if filter_strings(request.path):
                if request.method in ['POST', 'PUT']:

                    if request.body:
                        if request.content_type.startswith('multipart/form-data'):
                            pass
                        else:
                            try:
                                body = decrypt_aes256(request.body)
                                request._body = body

                            except Exception as e:

                                traceback.print_exc()
                                return JsonResponse({'error': str(e)}, status=400)
        except OperationalError as e:
            traceback.print_exc()


    def process_response(self, request, response):
        if filter_strings(request.path):
            if request.method in ['POST','GET','PUT']:
                if isinstance(response,Response):
                    response_content = json.dumps(response.data, cls=DjangoJSONEncoder)
                    try:
                        encrypted_data = encrypt_aes256(response_content.encode('utf-8'))
                    except Exception as e:

                        return response
                    response.data = {'data': encrypted_data.decode('utf-8')}
                    response.content = json.dumps(response.data)

                    return response

        return response

