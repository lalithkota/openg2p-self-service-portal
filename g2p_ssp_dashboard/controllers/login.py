import logging

from odoo import http
from odoo.http import request

from odoo.addons.auth_oauth.controllers.main import OAuthController, OAuthLogin, fragment_to_query_string

_logger = logging.getLogger(__name__)


class SSPLoginContorller(http.Controller):
    @http.route(["/ssp/login"], type="http", auth="public")
    def ssp_login(self, **kwargs):
        request.params["redirect"] = "/"

        providers = [
            p for p in OAuthLogin().list_providers() if p.get("g2p_ssp_allowed", False)
        ]
        return request.render(
            "g2p_ssp_dashboard.g2p_ssp_login_page", {"providers": providers}
        )


class SSPSigninController(OAuthController):
    @http.route("/ssp/signin", type="http", auth="none")
    @fragment_to_query_string
    def signin(self, **kw):
        return super(SSPSigninController, self).signin(**kw)
