
from odoo import models, fields, api
from odoo.exceptions import UserError


# This model inherits from the customer model of the crm module
class CrmCustomer(models.Model):
    _inherit = "res.partner"

    patient_id = fields.Many2one(
        comodel_name="hms.patient",
        string="Patient",
        help="Patient associated with this customer",
    )

    vat = fields.Char(string="Tax ID", required=True)


    # Constraint to prevent linking customer with email already in patient model
    @api.constrains("email", "patient_id")
    def _check_email_not_in_patient(self):
        for record in self:
            if record.email:
                # Check if the email exists in the hms.patient model
                existing_patient = self.env["hms.patient"].search(
                    [("email", "=", record.email)], limit=1
                )
                if existing_patient:
                    raise UserError(
                        f"The email '{record.email}' is already associated with a patient."
                    )



    def unlink(self):
        for record in self:
            if record.patient_id:
                raise UserError(
                    f"You cannot delete the customer '{record.name}' because it is linked to a patient."
                )
        return super(CrmCustomer, self).unlink()