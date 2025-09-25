from statement.parser.Base import Base
import pdfplumber
import pandas as pd

from pprint import pprint
from statement.models import Transaction
import io

class Maharashtra(Base):
    DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, filepath,company_id):
        super().__init__(company_id)
        self.df_list = []
        self.frame = None
        # http = urllib3.PoolManager()
        temp = io.BytesIO(filepath.read())
        # temp.write(http.request("GET", filepath).data)
        with pdfplumber.open(temp) as pdf:
            first_page = pdf.pages[0]
            table = first_page.extract_tables()
            table = table[1][1:]
            columns = [each.replace("\n","") for each in table[0]]
            print(columns)
            df = pd.DataFrame(table[1:], columns=columns)
            df.replace(to_replace='\n', value=' ', inplace=True, limit=None, regex=True, method='pad')
            self.df_list.append(df)
        for page in pdf.pages[1:-1]:
            table = page.extract_tables()
            table = table[0][1:]
            df = pd.DataFrame(table[1:], columns=columns)

            df.replace(to_replace='\n', value=' ', inplace=True, limit=None, regex=True, method='pad')
            self.df_list.append(df)
        self.frame = pd.concat(self.df_list)

    def get_parsed_frame(self, bank_obj=None, stat_bank_upl_obj=None):

        df1 = self.frame[self.frame['Date'].notna()]
        df1.reset_index(drop=True, inplace=True)
        frame = df1.where(pd.notnull(df1), None)
        rows_statements = []
        startDate, endDate = None, None
        # print(frame)
        for index, row in frame.iterrows():

            date, description, reference, debit, credit = (
                row['Date'], row['Particulars'], row['Cheque/Reference No'], row['Debit'], row['Credit'])
            date = self.convert_date_format(date)
            if not self.check_date_range(date):
                if not credit or credit is None:
                    credit = 0
                else:
                    credit = credit.replace(",", "")
                    credit = float(credit)
                if not debit or debit is None:
                    debit = 0
                else:
                    debit = debit.replace(",", "")
                    debit = float(debit)
                balance = debit if debit else credit
                stat = Transaction(file_id=stat_bank_upl_obj, date=date, description=description,
                                 reference=reference, credit=credit,
                                 debit=debit,
                                 balance=balance)
                rows_statements.append(stat)
            if index == 0:
                startDate = date
            else:
                endDate = date
        print("Successfully parsed statements")
        return rows_statements, startDate, endDate
#         print("HERE")
# from statement.parser.Maharashtra import Maharashtra
# obj = Maharashtra(r"C:\Users\AbdulRashid\Desktop\BlessedTree\jupyter notebook\sample_mh.pdf")
# obj.get_parsed_frame()