from odoo import models, fields, _, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        print("yes working")
        # doing the  custom code here
        return res


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # inherit these things for chatter purpose(footer)
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s - %s' % (field.name_seq, field.patient_name)))
        return res

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValueError(_('The Age Must be Greater than 5'))

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:  # in form view handles just one age group,but in tree view it handles multiple age group for that reason we have to use a loop for multiple values
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
        count = self.env['hospital.appointment'].search_count(
            [('patient_id', '=', self.id)])  # take all appointments of a patient and count it
        self.appointment_count = count

    def action_send_card(self):
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    @api.onchange('doctor')
    def set_doctor_gender(self):
        for rec in self:
            rec.doctor_gender = rec.doctor.gender

    patient_name = fields.Char(string='Name', required=True, track_visibility='always')
    patient_age = fields.Integer('Age',
                                 track_visibility='always')  # track visibility is using for when a user change age then it shows in chatter box
    notes = fields.Text(string="Notes")
    image = fields.Binary(string="Image")
    name = fields.Char(string='Test')
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))  # when you create item it preserves the order
    user_id = fields.Many2one('res.users', string='PRO')
    email = fields.Char(string="email")
    doctor = fields.Many2one('hospital.doctor', string="Doctor")

    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string="Gender")
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string="Gender")

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string="Age Group", compute='set_age_group')  # call 'set_age_group' function
    appointment_count = fields.Integer(string='Appointment',
                                       compute='get_appointment_count')  # using 'get_appointment_count' method
    active = fields.Boolean("Active", default=True)

    # when we create an item it maintains a sequence order
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    patient_name_upper = fields.Char(compute='_compute_upper_name', inverse='_inverse_upper_name')

    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name else False

    def test_crone_job(self):
        print('testing 1   2   3')
        # code accordingly to execute the cron
