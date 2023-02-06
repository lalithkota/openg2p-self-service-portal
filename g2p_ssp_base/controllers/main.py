from odoo import http
from odoo.http import request

from odoo.addons.auth_oidc.controllers.main import OpenIDLogin


class SSPBaseContorller(http.Controller):
    @http.route(["/ssp"], type="http", auth="public")
    def ssp_root(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/home")
        else:
            return request.redirect("/login")

    @http.route(["/ssp/login"], type="http", auth="public")
    def ssp_login(self, **kwargs):
        request.params["redirect"] = "/"
        context = {}

        context.update(
            dict(
                providers=[
                    p
                    for p in OpenIDLogin().list_providers()
                    if p.get("g2p_ssp_allowed", False)
                ]
            )
        )
        return request.render("g2p_ssp_base.g2p_ssp_login_page", qcontext=context)

    @http.route(["/ssp/logo.png"], type="http", auth="public")
    def ssp_logo(self, **kwargs):
        config = request.env["ir.config_parameter"].sudo()
        attachment_id = config.get_param("g2p_ssp_base.ssp_logo_attachment")
        return request.redirect("/web/content/%s" % attachment_id)
