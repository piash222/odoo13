from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = {'hospital.patient': 'related_patient_id'}
    _description = "Doctor Record"
    _rec_name = 'name'

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s ' % (field.name, )))
        return res

    name = fields.Char(string="Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female')
    ], default='male', string='Gender')
    user_id = fields.Many2one('res.users', string='Related_fields')
    patient_id = fields.Many2one('hospital.patient', string="Related Patient")
    related_patient_id = fields.Many2one('hospital.patient', string="Related Patient ID")

