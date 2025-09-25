from rest_framework.permissions import BasePermission
from company.models import Company,Branch
import json
import base64
import json
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

AES_KEY = base64.b64decode(os.environ.get('AES_KEY'))
AES_IV = base64.b64decode(os.environ.get('AES_IV'))
def decrypt_aes256(data: bytes) -> bytes:
    data = base64.b64decode(data)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    return unpadder.update(decrypted) + unpadder.finalize()

class CustomPermission(BasePermission):
    message = 'User is not owner of company'
    # def sub_user_access(self,user,request):
    #     if request
    def has_permission(self, request, view):

        if request.path.startswith('/userList/'):

            user = request.user
            if user and user.is_authenticated:
                return True

        if request.path.startswith('/registration/') or request.path.startswith('/server') \
                or request.path.startswith('/integration/token/refresh/'):
            return True

        user = request.user
        print(user.is_admin,"****************")
        if user.role == 'admin' and request.path.startswith('/subuser/') :
            return True
        if user.role != 'admin' and request.path.startswith('/subuser/'):
            return False
        if user.role != 'admin':
            access = user.user_access.all()
            if access:
                access = access[0]
            else:
                self.message = "No Access Found"
                return False
            user = user.sub_users.all()[0]

        if user and user.is_authenticated:
            if not user.subscribe.get_plan_subscribe():
                self.message = 'User Payment is not paid'
                return False
            if request.path.startswith('/integration/'):
                return True
            if request.method == 'GET':
                company_id = view.kwargs.get('comp_id',view.kwargs.get('company_id'))
                branch_id = view.kwargs.get('branch_id', view.kwargs.get('branch_id'))

                if company_id:
                    try:
                        comp = Company.objects.get(company_id=company_id)
                        print(comp.user,user,comp.user == user)
                        if comp.user == user:
                            if request.path.startswith('/company/') or request.path.startswith('/coa/') or request.path.startswith('/report/'):
                                return True
                            if branch_id:
                                return user.user_access.all()[0].branches.filter(branch_id=branch_id)
                            else:
                                return False

                        else:
                            # self.message = 'You are not owner'
                            return False
                    except:
                        pass
                else:
                    return True
            if request.method in ['POST','PUT']:

                company_id = None
                try:

                    dt = request.data
                    dt._mutable=True

                    data = dt['data']
                    data = decrypt_aes256(data)

                    data = eval(data)
                    data = json.loads(data)

                    company_id = data.get('company_id')
                    branch_id = data.get('branch_id')
                    dt['data'] = json.dumps(data)
                    dt._mutable=False

                except Exception as e:
                    print(e)
                    company_id = request.data.get('company_id')
                    branch_id = request.data.get('branch_id')

                if (request.path.startswith('/company/') or request.path.startswith('/integration/') or request.path.startswith('/payment/')) and request.user.role == "admin":
                    if request.method in ["PUT","POST"]:
                        return True


                try:
                    comp = Company.objects.get(company_id=company_id)

                    if comp.user == user:
                        if branch_id:
                            return user.user_access.all()[0].branches.filter(branch_id=branch_id).exists()
                    else:
                        return False
                except:
                    pass
        else:
            self.message = 'User is not Authenticated'
            return False


class SubUserPermission(BasePermission):
    pass