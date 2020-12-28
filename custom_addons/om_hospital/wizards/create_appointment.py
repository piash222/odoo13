from odoo import models, fields, api, _


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date = fields.Date(string="Appointment date")

    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            # Patient_Id is a many2one field so when access patient_ID you will be getting value as a recordset
            # like hospital.patient(1), to get the ID you gave use record.id
            'appointment_date': self.appointment_date
        }
        self.patient_id.message_post(body='Appointment Created Successfully', subject='Appointment creation')
        self.env['hospital.appointment'].create(vals)

    def get_data(self):
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', 3)])  # domain inside search
        for rec in appointments:
            print("appointment name", rec.name)
        print(appointments)
        return {
            'type': 'ir.actions.do_nothing'
        }
