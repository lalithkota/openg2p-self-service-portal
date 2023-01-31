from odoo import fields, models


class G2PSSPOauthProvider(models.Model):
    _inherit = "auth.oauth.provider"

    g2p_ssp_allowed = fields.Boolean("Allowed in SSP", default=False)
