
import pandas as pd
from statement.models import FileUpload
from datetime import datetime
import traceback
from dateutil import parser
class Base:
    GLOBAL_DATE_FORMAT = "%Y-%m-%d"

    def __init__(self,company_id):
        objs = FileUpload.objects.filter(company_id=company_id,bank_id__name=self.__class__.__name__)
        self.ranges = []
        for each in objs:
            if each.start_date and each.end_date:
                self.ranges.append([str(each.start_date), str(each.end_date)])
        print(self.ranges)
        #
        self.df = pd.DataFrame()

    def convert_date_format(self,date):
        date = parser.parse(date, fuzzy=True)
        # d = datetime.strptime(str(date.date), self.DATE_FORMAT)
        date = date.strftime(self.GLOBAL_DATE_FORMAT)
        return date

    def check_date_range(self,date):
        for each in self.ranges:
            start = each[0]
            end = each[1]
            if start <= date <= end:
                return True
        else:
            return False

    def parse_statement(self,bank_obj,stat_bank_upl_obj,company):
        rows_statements = []
        try:
            rows_statements,startDate,endDate =  self.get_parsed_frame(bank_obj,stat_bank_upl_obj)
            stat_bank_upl_obj.parse = True
            if not FileUpload.objects.filter(company_id=company,start_date=startDate,end_date=endDate):
                stat_bank_upl_obj.start_date = startDate
                stat_bank_upl_obj.end_date = endDate
            else:
                stat_bank_upl_obj.error_message = "File already uploaded"
                stat_bank_upl_obj.error = True
        except Exception as e:
            traceback.print_exc()
            print(e)
            errorMessage = str(e)
            stat_bank_upl_obj.error_message = "File Cannot be Parsed"
            stat_bank_upl_obj.error = True
            stat_bank_upl_obj.error = True
        stat_bank_upl_obj.save()
        return rows_statements