# Author: NICA-CREATOR desde Nicaragua 
# Copyright 2021 

{
    'name': 'Kardex for product',
    'version': '14.0.1.1.1',
    'price': 50.00,
    'currency':'USD',
    'support':'gtnorw@yahoo.com',   
    'category': 'Reporting',
    'summary': 'Kardex Report in Excel and  pdf Format, so display the records of products in a table',   
    'author': 'NICA-CREATOR', 
    "depends": ["base", "stock", "stock_account"],
    'images': ['static/description/main_screenshot.png'],
    'data': ['kardex.xml',"karde_report.xml","security/ir.model.access.csv",],
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'OPL-1',
}
