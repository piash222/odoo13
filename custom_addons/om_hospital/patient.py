from odoo import models, fields, _, api

class SalesOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'

    name = fields.Char(string='Test', required=True)
    patient_name = fields.Char(string='Name', required=True)
    patient_age = fields.Integer(string='age')
    notes = fields.Text(string='Notes')
    image = fields.Binary(string='Image')
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result