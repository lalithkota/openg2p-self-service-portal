from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings"]

    self_service_logo = fields.Many2one(
        "ir.attachment",
        config_parameter="g2p_self_service_base.self_service_logo_attachment",
    )
