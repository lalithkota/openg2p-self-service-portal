from odoo import http
from odoo.http import request


class SelfServiceDashboardContorller(http.Controller):
    @http.route(["/selfservice/home"], type="http", auth="user")
    def self_service_dashboard(self, **kwargs):
        return request.render(
            "g2p_self_service_dashboard.g2p_self_service_dashboard", {}
        )
