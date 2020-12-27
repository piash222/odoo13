from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'hospital.lab'
    _description = 'Hospital Laboratory'

    name = fields.Char(string="Name", required=True)
    user_id = fields.Many2one('res.users', string='responsible')
