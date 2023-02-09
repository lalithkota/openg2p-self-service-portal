from odoo import http
from odoo.http import request

from odoo.addons.auth_oidc.controllers.main import OpenIDLogin


class SelfServiceBaseContorller(http.Controller):
    @http.route(["/selfservice"], type="http", auth="user")
    def self_service_root(self, **kwargs):
        return request.redirect("/home")

    @http.route(["/selfservice/login"], type="http", auth="public")
    def self_service_login(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/home")
        request.params["redirect"] = "/"
        context = {}

        context.update(
            dict(
                providers=[
                    p
                    for p in OpenIDLogin().list_providers()
                    if p.get("g2p_self_service_allowed", False)
                ]
            )
        )
        return request.render("g2p_self_service_base.g2p_self_service_login_page", qcontext=context)

    @http.route(["/selfservice/logo.png"], type="http", auth="public")
    def self_service_logo(self, **kwargs):
        config = request.env["ir.config_parameter"].sudo()
        attachment_id = config.get_param("g2p_self_service_base.self_service_logo_attachment")
        return request.redirect("/web/content/%s" % attachment_id)
