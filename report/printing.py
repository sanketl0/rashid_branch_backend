# from datetime import date
# from multiprocessing import context
# from django.shortcuts import render
# import pdfkit
# import os
# from pathlib import Path
from datetime import datetime
# #Balnce Sheet Responce Converting Section 
# #Responce Convertig is the account type  wise 
# #becasue Ui Requirements so change the responce
# #Two unique account type Liabilites and Equites and Assest 
# def convert_balance_sheet_response(input_response):
    
#     # Creating acctype wise dictionary add the data below code
#     unique_acc_type = {"Liabilities & Equities": {}, "Assets": {}}

#     for x in input_response:
#         if x['acc_type'] in ('Liabilities', 'Equity'):
#             unique_acc_type["Liabilities & Equities"][x['acc_type']] = {}
#         else:
#             unique_acc_type["Assets"][x['acc_type']] = {}

#     for x in input_response:
#         if x['acc_type'] in ('Liabilities', 'Equity'):
#             unique_acc_type["Liabilities & Equities"][x['acc_type']][x['acc_head']] = {}
#         else:
#             unique_acc_type["Assets"][x['acc_type']][x['acc_head']] = {}

#     for x in input_response:
#         if x['acc_type'] in ('Liabilities', 'Equity'):
#             unique_acc_type["Liabilities & Equities"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}
#         else:
#             unique_acc_type["Assets"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}

#     for x in input_response:
#         if x['acc_type'] in ('Liabilities', 'Equity'):
#             try:
#                 unique_acc_type["Liabilities & Equities"][x['acc_type']][x['acc_head']][x['acc_subhead']][
#                     x['account_name']] += x['debitcredit']
#             except KeyError:
#                 unique_acc_type["Liabilities & Equities"][x['acc_type']][x['acc_head']][x['acc_subhead']][
#                     x['account_name']] = x['debitcredit']
#         else:
#             try:
#                 unique_acc_type["Assets"][x['acc_type']][x['acc_head']][x['acc_subhead']][x['account_name']] += x['debitcredit']
#             except KeyError:
#                 unique_acc_type["Assets"][x['acc_type']][x['acc_head']][x['acc_subhead']][x['account_name']] = x['debitcredit']
           
#     return unique_acc_type

# # def convert_balance_sheet_response(input_response):
#     # Creating acctype wise dictionary
#     # unique_acc_type = {"Liabilities & Equities": {}, "Assets": {}}

#     # for x in input_response:
#     #     acc_type = x['acc_type']
#     #     acc_head = x['acc_head']
#     #     acc_subhead = x['acc_subhead']
#     #     account_name = x['account_name']
#     #     debitcredit = x['debitcredit']

#     #     if acc_type in ('Liabilities', 'Equity'):
#     #         if acc_type not in unique_acc_type["Liabilities & Equities"]:
#     #             unique_acc_type["Liabilities & Equities"][acc_type] = {}
#     #         if acc_head not in unique_acc_type["Liabilities & Equities"][acc_type]:
#     #             unique_acc_type["Liabilities & Equities"][acc_type][acc_head] = {}
#     #         if acc_subhead not in unique_acc_type["Liabilities & Equities"][acc_type][acc_head]:
#     #             unique_acc_type["Liabilities & Equities"][acc_type][acc_head][acc_subhead] = {}

#     #         unique_acc_type["Liabilities & Equities"][acc_type][acc_head][acc_subhead][account_name] = \
#     #             unique_acc_type["Liabilities & Equities"][acc_type][acc_head][acc_subhead].get(account_name, 0) + debitcredit
#     #     else:
#     #         if acc_type not in unique_acc_type["Assets"]:
#     #             unique_acc_type["Assets"][acc_type] = {}
#     #         if acc_head not in unique_acc_type["Assets"][acc_type]:
#     #             unique_acc_type["Assets"][acc_type][acc_head] = {}
#     #         if acc_subhead not in unique_acc_type["Assets"][acc_type][acc_head]:
#     #             unique_acc_type["Assets"][acc_type][acc_head][acc_subhead] = {}

#     #         unique_acc_type["Assets"][acc_type][acc_head][acc_subhead][account_name] = \
#     #             unique_acc_type["Assets"][acc_type][acc_head][acc_subhead].get(account_name, 0) + debitcredit

#     # return unique_acc_type


    
# from importlib.resources import contents   
# def print_balance_sheet(response_data, output_path):
#     html = render(None, 'ba_html.html', context={"bill_items": response_data['data'],
#                                                  'total_data': response_data['total'],
#                                                  'Liabilities_Equity_sum':response_data['total']['Liabilities_Equity_sum'],
#                                                  'Assets_sum':response_data['total']['Assets_sum'],
#                                                  'profit':response_data['profit_loss']['profit'],
#                                                  'loss':response_data['profit_loss']['loss'],
                                              
#                                                  'company': response_data['company']})
#     print("6666666666666666666666666666666666666",context)
    
#     config = pdfkit.configuration(
#         wkhtmltopdf=os.path.join(Path(__file__).parent, r'wkhtmltox\bin\wkhtmltopdf.exe'))
#     pdfkit.from_string(html.content.decode(), output_path, configuration=config)

# #     return output_path
# # def print_balance_sheet(response_data, output_path):
# #     bill_items = response_data.get('data', [])
# #     total_data = response_data.get('total', {})
# #     Liabilities_Equity_sum = total_data.get('Liabilities_Equity_sum', 0)
# #     Assets_sum = total_data.get('Assets_sum', 0)
# #     profit_loss = response_data.get('profit_loss', {})
# #     profit = profit_loss.get('profit', 0)
# #     loss = profit_loss.get('loss', 0)
# #     company = response_data.get('company', {})

# #     html = render(None, 'ba_html.html', context={
# #         "bill_items": bill_items,
# #         'total_data': total_data,
# #         'Liabilities_Equity_sum': Liabilities_Equity_sum,
# #         'Assets_sum': Assets_sum,
# #         'profit': profit,
# #         'loss': loss,
# #         'company': company
# #     })

# #     print("6666666666666666666666666666666666666", context)

# #     config = pdfkit.configuration(
# #         wkhtmltopdf=os.path.join(Path(__file__).parent, r'wkhtmltox\bin\wkhtmltopdf.exe'))
# #     pdfkit.from_string(html.content.decode(), output_path, configuration=config)

# #     return output_path


# # # Thsi Converted Respose for Profit and Loss
# # #Group Respose
# # def convert_profit_loss_response(input_response):
# #     unique_acc_type = {"Income": {}, "Expense": {}}

# #     for x in input_response:
# #         if x['acc_type'] in ('Income'):
# #             unique_acc_type["Income"][x['acc_type']] = {}
# #         else:
# #             unique_acc_type["Expense"][x['acc_type']] = {}

# #     for x in input_response:
# #         if x['acc_type'] in ('Income'):
# #             unique_acc_type["Income"][x['acc_type']][x['acc_head']] = {}
# #         else:
# #             unique_acc_type["Expense"][x['acc_type']][x['acc_head']] = {}

# #     for x in input_response:
# #         if x['acc_type'] in ('Income'):
# #             unique_acc_type["Income"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}
# #         else:
# #             unique_acc_type["Expense"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}

# #     for x in input_response:
# #         if x['acc_type'] in ('Income'):
# #             unique_acc_type["Income"][x['acc_type']][x['acc_head']][x['acc_subhead']][
# #                 x['account_name']] = x['debit']
# #         else:
# #             unique_acc_type["Expense"][x['acc_type']][x['acc_head']][x['acc_subhead']][x['account_name']] = x[
# #                 'debitcredit']

# #     return unique_acc_type

from datetime import date
from multiprocessing import context
from django.shortcuts import render

import os
from pathlib import Path

#Balnce Sheet Responce Converting Section 
#Responce Convertig is the account type  wise 
#becasue Ui Requirements so change the responce
#Two unique account type Liabilites and Equites and Assest 
def convert_balance_sheet_response(input_response):
    
    # Creating acctype wise dictionary add the data below code
    unique_acc_type = {"Liabilities & Equities": {}, "Assets": {}}

    for x in input_response:
        if x['acc_type'] in ('Liabilities', 'Equity'):
            unique_acc_type["Liabilities & Equities"][x['acc_type']] = {}
        else:
            unique_acc_type["Assets"][x['acc_type']] = {}

    for x in input_response:
        if x['acc_type'] in ('Liabilities', 'Equity'):
            unique_acc_type["Liabilities & Equities"][x['acc_type']][x['acc_head']] = {}
        else:
            unique_acc_type["Assets"][x['acc_type']][x['acc_head']] = {}

    for x in input_response:
        if x['acc_type'] in ('Liabilities', 'Equity'):
            unique_acc_type["Liabilities & Equities"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}
        else:
            unique_acc_type["Assets"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}

    for x in input_response:
        if x['acc_type'] in ('Liabilities', 'Equity'):
            try:
                unique_acc_type["Liabilities & Equities"][x['acc_type']][x['acc_head']][x['acc_subhead']][
                    x['account_name']] += x['debitcredit']
            except KeyError:
                unique_acc_type["Liabilities & Equities"][x['acc_type']][x['acc_head']][x['acc_subhead']][
                    x['account_name']] = x['debitcredit']
        else:
            try:
                unique_acc_type["Assets"][x['acc_type']][x['acc_head']][x['acc_subhead']][x['account_name']] += x['debitcredit']
            except KeyError:
                unique_acc_type["Assets"][x['acc_type']][x['acc_head']][x['acc_subhead']][x['account_name']] = x['debitcredit']
           
    return unique_acc_type


    
from importlib.resources import contents   
def print_balance_sheet(response_data):
    current_date = str(datetime.now().strftime("%Y-%m-%d"))
    html = render(None, 'ba_html.html', context={"bill_items": response_data['data'],
                                                 'total_data': response_data['total'],
                                                 'Liabilities_Equity_sum':response_data['total']['Liabilities_Equity_sum'],
                                                 'Assets_sum':response_data['total']['Assets_sum'],
                                                 'profit':response_data['profit_loss']['profit'],
                                                 'loss':response_data['profit_loss']['loss'],
                                                  'current_date':current_date,
                                                 'company_name':response_data['company_name'],
                                                 'company': response_data['company']})
    print(response_data['company'][0])

    return html

def print_balance_sheet_v1(response_data):
    html = render(None, 'ba_v1_html.html',response_data)
    return html