from odoo import fields, models


class G2PServiceProviderOauthProvider(models.Model):
    _inherit = "auth.oauth.provider"

    g2p_service_provider_allowed = fields.Boolean("Allowed in Service Provider Portal", default=False)
