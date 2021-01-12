from odoo import models, fields, api, _
import pytz, datetime


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # inherit these things for chatter purpose(footer)
    # _order = "id desc"  # take the order where latest id shows on top
    _order = "appointment_date desc"

    def action_confirm(self):  # a button name in xml file file which name is 'action_confirm'
        for rec in self:  # once the button is clicked then the state is change into 'confirm'
            rec.state = 'confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'appointment Confirmed',
                    'type': 'rainbow_man'
                }
            }

    def action_done(self):
        for rec in self:
            rec.state = 'done'  # state tuple is defined below the code

    # when we create an item it maintains a sequence order
    @api.model
    def default_get(self, fields_list):
        res = super(HospitalAppointment, self).default_get(fields_list)
        print('test')
        res['patient_id'] = 1
        res['appointment_datetime'] = datetime.datetime.now()
        res['appointment_date'] = datetime.datetime.now()

        return res

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _(
                'New')  # using sequence for creating a seq order
        result = super(HospitalAppointment, self).create(vals)
        return result

    # @api.multi  'multi' is removed from Odoo 13.0 as it will be default.
    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        print('test write/n/n/n/n/n/n')
        return res

    def delete_lines(self):
        for rec in self:
            print("time in UTC", rec.appointment_datetime)
            # user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            # print('user_tz ', user_tz)
            # date_today = pytz.utc.localize(rec.appointment_datetime).astimezone(user_tz)
            # print('time in local timezone..', date_today)
            rec.appointment_lines = [(5, 0, 0)]

    # def get_default_note(self):
    # return "Subscribe Our Youtube channel"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    name = fields.Char(string='Appointment_ID', require=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    amount = fields.Float(
        string='Amount',
        required=False)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    doctor_ids = fields.Many2many('hospital.doctor', string='Doctors', required=True)
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note")  # using default note
    doctor_note = fields.Text(string="Doctor's Note")  # using default note
    pharmacy_note = fields.Text(string="Pharmacy Note")  # using default note
    appointment_date = fields.Date(string='Date')
    appointment_datetime = fields.Datetime(string='Date Time')
    appointment_lines = fields.One2many('hospital.appointment.lines', inverse_name='appointment_id',
                                        string="appointment_id")
    product_id = fields.Many2one('product.template', string='Product Template')

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            # lines = []
            print('self.product_id', self.product_id.product_variant_ids)
            for line in self.product_id.product_variant_ids:
                vals = {
                    'product_id': line.id,
                    'product_qty': 15
                }
                lines.append((0, 0, vals))
            print('lines', lines)
            rec.appointment_lines = lines

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=False)
    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='sale order',
        required=False)

    state = fields.Selection(selection=[  # declare the the state in status bar
        ('draft', 'Draft'),  # first item is using for database and 2nd item is using for frontend(odoo)
        ('confirm', 'Confirm'),
        ('done', 'Done')
    ], string='Status', readonly=True, default='draft')

    def action_notify(self):
        for rec in self:
            rec.doctor_id.user_id.notify_danger("Appointment")

    def test_recordset(self):
        for rec in self:
            print('odoo ORM: Record Set Operation')
            partners = rec.env['res.partner'].search([])
            print('partners', partners.mapped('name'))
            print('sorted  partners', partners.sorted(lambda o: o.create_date))
            print('filter  partners', partners.filter(lambda o: o.customer))


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment_lines'

    product_id = fields.Many2one('product.product', string="medicine ")
    product_qty = fields.Integer(string="quantity")
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')
