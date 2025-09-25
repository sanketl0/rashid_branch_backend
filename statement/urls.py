from django.urls import include, path
from statement.views import *

urlpatterns = [

    path('banks/',BankView.as_view()),
    path('file-upload/',FileUploadView.as_view()),
    path('file-upload/<uuid:company_id>/<uuid:branch_id>/',FileUploadView.as_view()),
    path('file-upload-name/<uuid:company_id>/<uuid:branch_id>/<str:filename>/',FileUploadView.as_view()),
    path('file-upload-bank/<uuid:company_id>/<uuid:branch_id>/<str:bank_name>/',FileUploadView.as_view()),
    # path('transactions/',TransactionView.as_view()),
    path('transactions/<uuid:file_id>',TransactionOldView.as_view()),
    path('bank-transactions/<uuid:file_id>',TransactionView.as_view()),
    path('transaction-details/',TransactionDetailView.as_view()),
    path('transaction-details/<uuid:transaction_id>',TransactionDetailView.as_view()),
    path('multipayment/',MultiPaymentView.as_view()),
    path('multipayment-made/',MultiPaymentMadeView.as_view()),


]