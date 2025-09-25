### Notes for migration to live server

Delete these migrations:

```
DELETE FROM django_migrations 
WHERE app in ('accounting', 'banking', 'coa', 'company', 'item', 'purchase', 'salescustomer', 'login')
```

Create these COA
``` sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

INSERT INTO coa (coa_id, account_type, account_head, account_subhead, account_name)
VALUES
        (uuid_generate_v4(), 'Liabilities', 'Current Liabilities', 'Other Current Liabilities', 'Output CGST'),
        (uuid_generate_v4(), 'Liabilities', 'Current Liabilities', 'Other Current Liabilities', 'Output IGST'),
        (uuid_generate_v4(), 'Liabilities', 'Current Liabilities', 'Other Current Liabilities', 'TCS Payable'),
        (uuid_generate_v4(), 'Liabilities', 'Current Liabilities', 'Other Current Liabilities', 'TDS Payable'),
        (uuid_generate_v4(), 'Assets', 'Current Assets', 'Other Current Assets', 'TCS Receivable'),
        (uuid_generate_v4(), 'Assets', 'Current Assets', 'Other Current Assets', 'TDS Receivable'),

        (uuid_generate_v4(), 'Assets', 'Current Assets', 'Other Current Assets', 'Input IGST'),
        (uuid_generate_v4(), 'Assets', 'Current Assets', 'Other Current Assets', 'Input CGST'),
        (uuid_generate_v4(), 'Assets', 'Current Assets', 'Other Current Assets', 'Input SGST')
  
```    

Update this COA `0eb6c6c6-ed0a-4521-8d33-b3127a0c5f3b`
```sql
UPDATE coa SET  "account_subhead"='Other Current Liabilities' WHERE coa_id='0eb6c6c6-ed0a-4521-8d33-b3127a0c5f3b'
```

``` sql
ALTER TABLE company ALTER COLUMN created_date TYPE TIMESTAMP;
ALTER TABLE company ALTER COLUMN modified_date TYPE TIMESTAMP;
ALTER TABLE company ALTER COLUMN deleted_date TYPE TIMESTAMP;
ALTER TABLE company_financialyear ALTER COLUMN created_date TYPE TIMESTAMP;
ALTER TABLE company_financialyear ALTER COLUMN modified_date TYPE TIMESTAMP;
ALTER TABLE company_financialyear ALTER COLUMN deleted_date TYPE TIMESTAMP;
```
"# rashid_branch_backend" 
