file_path = r"D:\ZBackup Autocount\September Autocount\All_Autocount\banking\models\__init__.py"

def change_case(str):
    res = [str[0].lower()]
    for c in str[1:]:
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            res.append('_')
            res.append(c.lower())
        else:
            res.append(c)
     
    return ''.join(res)

import os
with open(file_path, 'r') as f:
    
    classes = {}
    new_class = []
    start = False
    previous_file = None
    for line in f.readlines():
        if line.startswith('class'):
            start = True
            x = line.split(" ")[1].split("(")[0]
            model_file = change_case(x) + "_model.py"
            
            print(model_file)
                
            previous_file = model_file
            classes[previous_file] = new_class
            new_class = []
            previous_file = model_file
        if start:
            new_class.append(line)
        
    for key, value in classes.items():
        print(key)
        print(value)
        
#         with open(os.path.join(r"D:\ZBackup Autocount\September Autocount\All_Autocount\banking\models", key), 'w') as m:
#                     m.write("""
# from django.db import models
# import uuid
# from company.models import Company, Branch
# """)            
                
#                     m.writelines(value) 
        break
        print("----"*10)
        
            
            