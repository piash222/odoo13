from odoo import http


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
