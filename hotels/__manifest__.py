{
    'name': 'Hotels',
    'version': '1.0',
    'license': 'AGPL-3',
    'description': 'Hotels Management',
    'author': 'Vyacheslav Tatarkin',
    'depends': ['base'],
    'application': True,
    'installable': True,
    'auto_install': False,
    'data': [
        'views/hotel_view.xml',
        'views/contract_view.xml',
        'views/invoice_view.xml',
        'views/order_view.xml',
        'views/hotels_partner_view.xml',
        'security/ir.model.access.csv',
    ],
}
