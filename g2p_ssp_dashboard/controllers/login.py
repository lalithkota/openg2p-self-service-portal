import logging

from odoo import http
from odoo.http import request

from odoo.addons.auth_oauth.controllers import main as auth_oauth

_logger = logging.getLogger(__name__)


class SSPLoginContorller(http.Controller):
    @http.route(["/ssp/login"], type="http", auth="public")
    def ssp_login(self, **kwargs):
        request.params["redirect"] = "/"
        context = {}

        context.update(
            dict(
                providers=[
                    p
                    for p in auth_oauth.OAuthLogin().list_providers()
                    if p.get("g2p_ssp_allowed", False)
                ]
            )
        )
        return request.render("g2p_ssp_dashboard.g2p_ssp_login_page", qcontext=context)


class SSPSigninController(auth_oauth.OAuthController):
    @http.route("/ssp/signin", type="http", auth="none")
    @auth_oauth.fragment_to_query_string
    def signin(self, **kw):
        return super(SSPSigninController, self).signin(**kw)
