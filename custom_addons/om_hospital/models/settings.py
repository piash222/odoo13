from odoo import fields, models, api


class HospitalSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    note = fields.Char(string='Default Note')
    module_crm =  fields.Boolean("CRM")

    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('om_hospital.note', self.note)
        return res

    @api.model
    def get_values(self):
        res = super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        note = ICPSudo.get_param('om_hospital.note')
        res.update(
            note=note
        )
        return res
