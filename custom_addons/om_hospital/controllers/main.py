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
