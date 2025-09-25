from django.shortcuts import render
# import pdfkit
import os
from pathlib import Path

from datetime import datetime
# def convert_profit_loss_response(input_response):
#     unique_acc_type = {"Expenses": {}, "Income": {}}

#     for x in input_response:
#         if x['acc_type'] in ('Expenses'):
#             unique_acc_type["Expenses"][x['acc_type']] = {}
#         else:
#             unique_acc_type["Income"][x['acc_type']] = {}

#     for x in input_response:
#         if x['acc_type'] in ('Expenses'):
#             unique_acc_type["Expenses"][x['acc_type']][x['acc_head']] = {}
#         else:
#             unique_acc_type["Income"][x['acc_type']][x['acc_head']] = {}

#     for x in input_response:
#         if x['acc_type'] in ('Expenses'):
#             unique_acc_type["Expenses"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}
#         else:
#             unique_acc_type["Income"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}

#     for x in input_response:
#         if x['acc_type'] in ('Expenses'):
#             unique_acc_type["Expenses"][x['acc_type']][x['acc_head']][x['acc_subhead']][
#                 x['account_name']] = x['debit']
#         else:
#             unique_acc_type["Income"][x['acc_type']][x['acc_head']][x['acc_subhead']][x['account_name']] = x[
#                 'debitcredit']

#     return unique_acc_type



# convert the respone the profit loss 
#the printing time convet the respose fro ui s

def convert_profit_loss_response(input_response):
    unique_acc_type =  {"Expenses": {}, "Income": {}}

    for x in input_response:
        if x['acc_type'] in ('Expenses'):
            unique_acc_type["Expenses"][x['acc_type']] = {}
        else:
            unique_acc_type["Income"][x['acc_type']] = {}

    for x in input_response:
        if x['acc_type'] in ('Expenses'):
            unique_acc_type["Expenses"][x['acc_type']][x['acc_head']] = {}
        else:
            unique_acc_type["Income"][x['acc_type']][x['acc_head']] = {}

    for x in input_response:
        if x['acc_type'] in ('Expenses'):
            unique_acc_type["Expenses"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}
        else:
            unique_acc_type["Income"][x['acc_type']][x['acc_head']][x['acc_subhead']] = {}

    for x in input_response:
        if x['acc_type'] in ('Expenses'):
            try:
                unique_acc_type["Expenses"][x['acc_type']][x['acc_head']][x['acc_subhead']][
                    x['account_name']] += x['debitcredit']
            except KeyError:
                unique_acc_type["Expenses"][x['acc_type']][x['acc_head']][x['acc_subhead']][
                    x['account_name']] = x['debitcredit']
        else:
            try:
                unique_acc_type["Income"][x['acc_type']][x['acc_head']][x['acc_subhead']][x['account_name']] += x['debitcredit']
            except KeyError:
                unique_acc_type["Income"][x['acc_type']][x['acc_head']][x['acc_subhead']][x['account_name']] = x['debitcredit']
           
    return unique_acc_type



def print_pnl_sheet(response_data, output_path):
    current_date = str(datetime.now().strftime("%Y-%m-%d"))
    html = render(None, 'pnl_html.html', context={"bill_items": response_data['data'],
                                                 'total_data': response_data['total'], 
                                                 'Expenses_sum':response_data['total']['Expenses_sum'],
                                                 'Income_sum':response_data['total']['Income_sum'],
                                                 'profit':response_data['profit_loss']['profit'],
                                                 'loss':response_data['profit_loss']['loss'],
                                                  'current_date':current_date,
                                                 'company': response_data['company']})

    return html

