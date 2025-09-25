from statement.parser.Base import Base
import pdfplumber
import pandas as pd
from statement.models import Transaction
import io


class Icici(Base):
    DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, filepath,company_id):
        super().__init__(company_id)
        self.df_list = []
        self.frame = None
        # http = urllib3.PoolManager()
        file = io.BytesIO(filepath.read())
        data = []
        temp = ['', None, None, None, None, None, None, None,None]
        with pdfplumber.open(file) as pdf:
            pages = pdf.pages
            for index, page in enumerate(pages):
                print(f"page no {index + 1}")
                for table in page.extract_tables():
                    for row in table:
                        if list(row) != temp:
                            data.append(row)
                        else:
                            print(row)
        if data:

            columns = [each.replace("\n", "")  for each in data[0] if each]
            print(columns,data,"stage 1 >>>>>>>>>>")
            df = pd.DataFrame(data[1:], columns=columns)
            df = df.drop(columns=['No.', 'Value Date','ChequeNo.'])
            df.replace(to_replace='\n', value=' ', inplace=True, limit=None, regex=True, method='pad')
            new_column_names = ['reference', 'date','description','type','amount','balance']
            df.columns = new_column_names
            self.frame = df

    def get_parsed_frame(self, bank_obj=None, stat_bank_upl_obj=None):
        df1 = self.frame[self.frame['date'].notna()]
        df1.reset_index(drop=True, inplace=True)
        frame = df1.where(pd.notnull(df1), None)
        rows_statements = []
        startDate, endDate = None, None
        for index, row in frame.iterrows():
            reference,date, description,  tp, amount,balance = (
                row['reference'], row['date'], row['description'], row['type'], row['amount'],row['balance'])
            date = self.convert_date_format(date)
            if not self.check_date_range(date):
                if tp == "CR":
                    credit = float(amount.replace(",",""))
                    debit = 0
                else:
                    credit = 0
                    debit = float(amount.replace(",",""))
                if not credit or credit is None:
                    credit = 0
                balance = balance.replace(",","")
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


# obj = Icici(r"C:/Users/AbdulRashid/Downloads/OpTransactionHistoryUX304-11-2024.pdf")
# obj.get_parsed_frame()