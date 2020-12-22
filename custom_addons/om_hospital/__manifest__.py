{
    'name': "Hospital Management",
    'version': '13.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Module fo managing the Hospitals',
    'sequence': '10',
    'license': 'AGPL-3',
    'author': "Smart Technologies (BD) Ltd",
    'maintainer': 'Odoo Mates',
    'website': 'odoomates.com',
    'depends': ['sale'],
    'demo': [],
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/appointment_sequence.xml',
        'data/data.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'reports/report.xml',
        'reports/patient_card.xml',

    ],
    # data files containing optionally loaded demonstration data
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto install': False,
}

