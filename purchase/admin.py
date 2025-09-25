from django.contrib import admin
from purchase.models.Bill_model import Bill
from purchase.models.Paymentmade_model import PaymentMade
from purchase.models.Bill_Item_model import Bill_Item
from purchase.models.Expense_Record_model import ExpenseRecord
from purchase.models.Vendor_model import Vendor
from purchase.models.Debitnote_model import DebitNote
from banking.models import VendorAdvanced
from purchase.models.Tds_model import TDS
admin.site.register([Bill,PaymentMade,Bill_Item,ExpenseRecord,Vendor,DebitNote,VendorAdvanced,TDS])
# from .models import (Bill,
#                      Bill_Item,
#                      BillJournalTransaction,
#                      DebitItem,
#                      DebitNote,
#                      DebitNoteTransaction,
#                      ExpenseJournalTransaction,
#                      ExpenseRecord,
#                      PaymentMade,
#                      PaymentmadeJournalTransaction,
#                      PO,
#                      PoItem,
#                      TDS,
#                      VendorContact,
#                      Vendor
#                      )

# for m in (Bill,
#           Bill_Item,
#           BillJournalTransaction,
#           DebitItem,
#           DebitNote,
#           DebitNoteTransaction,
#           ExpenseJournalTransaction,
#           ExpenseRecord,
#           PaymentMade,
#           PaymentmadeJournalTransaction,
#           PO,
#           PoItem,
#           TDS,
#           VendorContact,
#           Vendor
#           ):
#     admin.site.register(m)
