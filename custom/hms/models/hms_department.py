from odoo import models, fields


class HmsDepartment(models.Model):
    _name = 'hms.department'
    _description = 'Department Medical Record'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    capacity = fields.Integer(string="Capacity", required=True)
    is_open = fields.Boolean(string="Is Opened", default=True)
    patient_ids = fields.One2many(comodel_name='hms.patient',inverse_name='department_id')
