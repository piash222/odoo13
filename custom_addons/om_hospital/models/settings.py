from odoo import fields, models, api
from ast import literal_eval


class HospitalSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    note = fields.Char(string='Default Note')
    module_crm = fields.Boolean("CRM")
    product_ids = fields.Many2many('product.product')

    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('om_hospital.note', self.note)
        print('test', self.product_ids.ids)
        self.env['ir.config_parameter'].set_param('om_hospital.product_ids', self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        note = ICPSudo.get_param('om_hospital.note')
        product_ids = self.env['ir.config_parameter'].sudo().get_param('om_hospital.product_ids')
        print(product_ids)
        res.update(
            note=note,
            product_ids=[[6, 0, literal_eval(product_ids)]]
        )
        return res
