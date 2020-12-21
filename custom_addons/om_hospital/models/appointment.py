from odoo import models, fields, api, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # inherit these things for chatter purpose(footer)
    #_order = "id desc"  # take the order where latest id shows on top
    _order = "appointment_date desc"

    def action_confirm(self): # a button name in xml file file which name is 'action_confirm'
        for rec in self:  # once the button is clicked then the state is change into 'confirm'
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'  # state tuple is defined below the code

    # when we create an item it maintains a sequence order
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New') # using sequence for creating a seq order
        result = super(HospitalAppointment, self).create(vals)
        return result

    #def get_default_note(self):
        #return "Subscribe Our Youtube channel"

    def get_default_note(self):
        return 1

    name = fields.Char(string='Appointment_ID',require=True,copy=False,readonly=True,
                       index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient',string='Patient',required=True,default=get_default_note)
    patient_age = fields.Integer('Age',related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note") # using default note
    appointment_date = fields.Date(string='Date',required=True)

    state = fields.Selection(selection=[  # declare the the state in status bar
        ('draft', 'Draft'),  # first item is using for database and 2nd item is using for frontend(odoo)
        ('confirm', 'Confirm'),
        ('done', 'Done')
    ], string='Status', readonly=True, default='draft')










