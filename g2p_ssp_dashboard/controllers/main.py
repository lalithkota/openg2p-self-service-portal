from odoo import http
from odoo.http import request


class SSPDashboardContorller(http.Controller):
    @http.route(["/ssp/home"], type="http", auth="user")
    def ssp_dashboard(self, **kwargs):
        return request.render("g2p_ssp_dashboard.g2p_ssp_dashboard", {})
