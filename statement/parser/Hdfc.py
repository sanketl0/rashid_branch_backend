from statement.parser.Base import Base
import pandas as pd
from datetime import datetime
from statement.models import Transaction,FileUpload
import tabula


class Hdfc(Base):
    DATE_FORMAT = "%d/%m/%y"

    def __init__(self,filepath,company_id):
        super().__init__(company_id)
        try:
            self.df_list = tabula.read_pdf(filepath, stream=True, guess=True, pages='all',
                                      multiple_tables=True,
                                      pandas_options={
                                          'header': None}
                                      )
            print(type(self.df_list))
        except Exception as e:
            print('The Error is', e)

    def get_parsed_frame(self,bank_obj,stat_bank_upl_obj):
        for each in self.df_list:
            self.df = self.df.append(each)
        self.df.reset_index(drop=True, inplace=True)
        self.df.columns = self.df.iloc[0]
        self.df = self.df[1:]
        print(self.df['Narration'].str.contains("STATEMENT SUMMARY"))
        print(self.df)
        print(self.df['Narration'])
        index_lst = self.df.index[self.df['Narration'].fillna('').str.contains("STATEMENT SUMMARY")].tolist()
        if index_lst:
            self.df = self.df.iloc[:index_lst[-1] - 1, :]
        date_indexes = self.df[self.df['Date'].notnull()].index.tolist()
        for index, each in enumerate(date_indexes):
            if index == len(date_indexes) - 1:
                string = ''.join(self.df.loc[each:self.df.index[-1]].Narration)
                # print(self.df.loc[self.df.index[-1]])
                self.df["Narration"][each] = string
            else:
                string = ''.join(self.df.loc[each:date_indexes[index + 1] - 1].Narration)
                self.df["Narration"][each] = string
        df1 = self.df[self.df['Date'].notna()]
        df1.reset_index(drop=True, inplace=True)
        frame = df1.where(pd.notnull(df1), None)
        rows_statements = []
        startDate,endDate = None,None
        for index, row in frame.iterrows():
            date, description, reference, debit, credit = (
            row['Date'], row['Narration'], row['Chq./Ref.No.'], row['Withdrawal Amt.'], row['Deposit Amt.'])
            date = self.convert_date_format(date)
            if not self.check_date_range(date):
                if credit is None:
                    credit = 0
                else:
                    credit = credit.replace(",", "")
                    credit = float(credit)
                if debit is None:
                    debit = 0
                else:
                    debit = debit.replace(",", "")
                    debit = float(debit)
                balance = debit if debit else credit
                stat = Transaction(file_id=stat_bank_upl_obj, date=date, description=description, reference=reference, credit=credit,
                                 debit=debit,
                                 balance=balance)
                rows_statements.append(stat)
            if index == 0:
                startDate = date
            else:
                endDate = date

        return rows_statements,startDate,endDate
