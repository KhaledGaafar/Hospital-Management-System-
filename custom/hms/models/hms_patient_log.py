from odoo import models, fields



class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log History'
    _rec = 'description'


    patient_id = fields.Many2one('hms.patient', string='Patient')
    created_by = fields.Many2one('hms.doctors')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    description = fields.Text()