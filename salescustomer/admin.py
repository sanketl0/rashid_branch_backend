from django.contrib import admin
from salescustomer.models.Estimate_model import Estimate
from salescustomer.models.Estimated_item_model import EstimatedItem
from salescustomer.models.Recurringinvoice_model import RI
from salescustomer.models.Invoice_model import Invoice
from salescustomer.models.Pr_model import PR
from salescustomer.models.Paymentmode_model import PaymentMode
from salescustomer.models.Invoice_item_model import InvoiceItem
from salescustomer.models.Paymentterms_model import PaymentTerms
from salescustomer.models.Salescustomer_model import SalesCustomer
from salescustomer.models.Employee_model import Employee
from salescustomer.models.Dc_model import DC
from salescustomer.models.So_model import SO
from salescustomer.models.Creditnote_model import CreditNote
from banking.models.customer_advance_model import CustomerAdvance
from salescustomer.models.Dc_item_model import DcItem
from salescustomer.models.Tcs_model import TCS
admin.site.register([Estimate,EstimatedItem,RI,Invoice,PR,PaymentTerms,CustomerAdvance,TCS,
                     PaymentMode,InvoiceItem,SalesCustomer,Employee,DC,SO,CreditNote,DcItem])
