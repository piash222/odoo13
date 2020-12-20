{
    'name': 'Hospital management',
    'version': '13.0.1.0.0',
    'category': 'Extra tools',
    'summary': 'Module for managing the Hospitals',
    'sequence': '10',
    'license': 'AGPL-3',
    'author': 'Shihab',
    'maintainer': 'Shihab Uddin',
    'website': '',
    'depends': ['mail', 'sale'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'patient.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

