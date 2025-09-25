from hmac import compare_digest


class Invoice:

    def __init__(self, coa_id, amount):
        self.coa_id = coa_id 
        self.amount = amount

invoices = [
    Invoice('coa1232', 1400),
    Invoice('coa1232', 5400),
    Invoice('coa5568', 1400),
    Invoice('coa9908', 5800),
]