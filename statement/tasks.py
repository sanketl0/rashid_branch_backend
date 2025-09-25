
from statement.models import FileUpload,Transaction,Bank
from django.conf import settings

from statement.parser.Maharashtra import Maharashtra
from statement.parser.Hdfc import  Hdfc
from statement.parser.icici import Icici
import os
from pathlib import Path
import traceback




def parseStatement(*args):
    print(args)
    file = args[0]
    filepath = file

    bank = args[1]
    bank_obj = Bank.objects.get(name=bank[0])
    stat_bank_upl_obj = FileUpload.objects.get(file_id=args[2])
    # print(bank,filepath,stat_bank_upl_obj)
    try:
        instance = eval(bank[0])(filepath,args[3])
        rows_statements = instance.parse_statement(bank_obj,stat_bank_upl_obj,args[3])
        msg = Transaction.objects.bulk_create(rows_statements)
        print(msg)
    except Exception as e:
        stat_bank_upl_obj.parse = False
        stat_bank_upl_obj.error = True
        stat_bank_upl_obj.error_message = "File Cannot be Parsed"
        stat_bank_upl_obj.save()
        traceback.print_exc()
        print(e)

    return "Done"