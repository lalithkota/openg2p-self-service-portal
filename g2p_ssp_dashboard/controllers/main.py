from odoo import http
from odoo.http import request


class SSPDashboardContorller(http.Controller):
    @http.route(["/ssp"], type="http", auth="public")
    def ssp_root(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/home")
        else:
            return request.redirect("/login")

    @http.route(["/ssp/home"], type="http", auth="user")
    def ssp_dashboard(self, **kwargs):
        return request.render("g2p_ssp_dashboard.g2p_ssp_dashboard", {})
