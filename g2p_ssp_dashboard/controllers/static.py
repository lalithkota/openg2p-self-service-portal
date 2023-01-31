import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class SSPStaticContorller(http.Controller):
    @http.route(["/ssp/login"], type="http", auth="public")
    def ssp_login(self, **kwargs):
        request.params["redirect"] = "/"

        return request.render("g2p_ssp_dashboard.g2p_ssp_login_page", {})
