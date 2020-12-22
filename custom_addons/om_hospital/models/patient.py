from odoo import models, fields, _, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # inherit these things for chatter purpose(footer)
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValueError(_('The Age Must be Greater than 5'))

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self: # in form view handles just one age group,but in tree view it handles multiple age group for that reason we have to use a loop for multiple values
            if rec.patient_age < 18:
                rec.age_group = 'minor'
            else:
                rec.age_group = 'major'

    # for smart button purpose(appointments button in patients page)
    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],  # take all appointments(patient id) of a patient
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)]) # take all appointments of a patient and count it
        self.appointment_count = count

    patient_name = fields.Char(string='Name', required=True,track_visibility='always')
    patient_age = fields.Integer('Age',track_visibility='always') # track visibility is using for when a user change age then it shows in chatter box
    notes = fields.Text(string="Notes")
    image = fields.Binary(string="Image")
    name = fields.Char(string='Test')
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New')) # when you create item it preserves the order
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male',string="Gender")

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor','Minor'),
    ], string="Age Group", compute='set_age_group')  # call 'set_age_group' function
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count') # using 'get_appointment_count' method

    # when we create an item it maintains a sequence order
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result


