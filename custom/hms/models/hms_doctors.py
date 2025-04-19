from odoo import models, fields,api


class HmsDoctors(models.Model):
    _name = 'hms.doctors'
    _description = 'Doctors Medical Record'



    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Binary(string="Image")

    department_id = fields.Many2one(
        comodel_name="hms.department", string="Department", required=True
    )
    patient_ids = fields.One2many(
        comodel_name="hms.patient", inverse_name="doctor_ids", string="Patients"
    )

    name = fields.Char(string="Name", compute="_compute_name", store=True)

    @api.depends("first_name", "last_name")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"