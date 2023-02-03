from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings"]

    ssp_logo = fields.Many2one(
        "ir.attachment", config_parameter="g2p_ssp_base.ssp_logo_attachment"
    )
