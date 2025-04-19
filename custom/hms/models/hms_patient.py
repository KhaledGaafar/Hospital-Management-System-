from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from dateutil.relativedelta import relativedelta
from datetime import date


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient Medical Record'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ])
    state = fields.Selection(
        selection=[
            ("undetermined", "Undetermined"),
            ("good", "Good"),
            ("fair", "Fair"),
            ("serious", "Serious"),
        ],
        string="Condition",
    )
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    birth_date = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
        readonly=True,
        help="Patient's age calculated from birth date"
    )
    email = fields.Char(
        string='Email',
        help="Patient's email address",
        tracking=True
    )
    department_id = fields.Many2one(comodel_name='hms.department',domain="[('is_opened','=',True)]")
    department_capacity = fields.Integer(related='department_id.capacity')
    doctor_ids = fields.Many2many(comodel_name='hms.doctors')
    log_history_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log History')


    @api.depends("first_name", "last_name")
    def _compute_name(self):
        for record in self:
            if not record.first_name and not record.last_name:
                record.first_name = "Your"
                record.last_name = "Name"
            elif not record.first_name:
                record.first_name = "Your"
            elif not record.last_name:
                record.last_name = "Name"

            record.name = f"{record.first_name} {record.last_name}"

    @api.constrains('pcr', 'cr_ratio')
    def _check_pcr_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked!")


    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30 and not self.pcr:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Checked",
                    'message': "PCR has been automatically checked because age is under 30",
                }
            }
    def change_state_good(self):
        for record in self:
            old_state = record.state
            record.state = "good"
            self.env["hms.patient.log"].create(
                {
                    "patient_id": record.id,
                    "description": f"State changed from {old_state} to Good",
                }
            )

    def change_state_fair(self):
        for record in self:
            old_state = record.state
            record.state = "fair"
            self.env["hms.patient.log"].create(
                {
                    "patient_id": record.id,
                    "description": f"State changed from {old_state} to Fair",
                }
            )

    def change_state_serious(self):
        for record in self:
            old_state = record.state
            record.state = "serious"
            self.env["hms.patient.log"].create(
                {
                "patient_id": record.id,
                "description": f"State changed from {old_state} to Serious",
                }
            )


    show_history = fields.Boolean(compute='_compute_show_history')

    @api.depends('age')
    def _compute_show_history(self):
        for record in self:
            record.show_history = record.age >= 50


    @api.constrains('email')
    def _check_valid_email(self):
        if self.email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', self.email):
            raise ValidationError("Please provide a valid email address")

    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'Email address must be unique per patient'),
    ]

    @api.depends('birth_date')
    def _compute_age(self):
        """Calculate age based on birth date"""
        today = date.today()
        for patient in self:
            if patient.birth_date:
                delta = relativedelta(today, patient.birth_date)
                patient.age = delta.years
            else:
                patient.age = 0
