from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleInherit, self).shop()
        print('inherited odoo mates')
        return res


class Hospital(http.Controller):
    # sample controller created
    @http.route('/hospital/patient/', website=True, auth="public")
    def hospital_patient(self, **kw):
        patients = http.request.env['hospital.patient'].sudo().search([])  # sudo to bypass all the access right
        print(f'patients---------------> patients, {type(patients)}')
        return http.request.render('om_hospital.patients_page', {
            'patients': patients
        })

    @http.route('/create_patient', type='json', auth='user')
    def create_patient(self, **rec):
        if http.request.jsonrequest:
            print('rec', rec)
            if rec['name']:
                vals = {
                    'patient_name': rec['name']
                }
                new_patient = http.request.env['hospital.patient'].sudo().create(vals)
                print(new_patient, 'is the patient')
                args = {
                    'success': True, 'message': 'Success', 'ID': new_patient.id
                }
                return args

    @http.route('/update_patient', type='json', auth='user')
    def update_patient(self, **rec):
        if http.request.jsonrequest:
            if rec['id']:
                patient = http.request.env['hospital.patient'].sudo().search([('id', "=", [rec['id']])])
                if patient:
                    patient.sudo().write(rec)
                args = {'success': True, 'message': 'Success'}
        return args

    @http.route('/get_patients', type='json', auth='user')
    def get_patient(self):
        print('yes here entered')
        patient_rec = http.request.env['hospital.patient'].search([])
        patients = []
        for rec in patient_rec:
            vals = {
                'id': rec.id,
                'name': rec.patient_name,
                'sequence': rec.name_seq
            }
            patients.append(vals)
        print(patients, '<------patient list')
        data = {
            'status': 200, 'response': patients, 'messages': 'Done All Patients Returned'
        }
        return data
    @http.route('/om_hospital/appointments', auth='user', type='json')
    def appointment_banner(self):
        return {
            'html': """
                <div>
                <link>
                <center>
                <h1> <font color="red">Like and subscribe the channel....</font></h1>
                </center>
                <center>
                <p>
                <font color='blue'><a href='https://www.youtube.com'>search youtube for videos</a></font>
                </p>
                </link>
                </center>
                </div>
            """
        }
