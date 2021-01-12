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
    'depends': ['sale', 'sale_stock', 'board'],
    'demo': [],
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/appointment_sequence.xml',
        'data/data.xml',
        'data/cron.xml',
        'data/mail_template.xml',
        'wizards/create_appointment.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        'views/lab.xml',
        'views/settings.xml',
        'views/sale_view.xml',
        'reports/sale_report_inherit.xml',
        'reports/report.xml',
        'reports/patient_card.xml',
        'views/template.xml',
        'views/dashboard.xml',
        'views/server_action.xml',
        'views/partner_view.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto install': False,
}
