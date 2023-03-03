import json
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from math import ceil

from odoo import http
from odoo.http import request

from odoo.addons.auth_oidc.controllers.main import OpenIDLogin

_logger = logging.getLogger(__name__)


class SelfServiceContorller(http.Controller):
    @http.route(["/selfservice"], type="http", auth="public", website=True)
    def self_service_root(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/selfservice/home")
        else:
            return request.redirect("/selfservice/login")

    @http.route(["/selfservice/login"], type="http", auth="public", website=True)
    def self_service_login(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/selfservice/home")
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
        return request.render("g2p_self_service_portal.login_page", qcontext=context)

    @http.route(["/selfservice/logo"], type="http", auth="public", website=True)
    def self_service_logo(self, **kwargs):
        config = request.env["ir.config_parameter"].sudo()
        attachment_id = config.get_param(
            "g2p_self_service_portal.self_service_logo_attachment"
        )
        return request.redirect("/web/content/%s" % attachment_id)

    @http.route(["/selfservice/myprofile"], type="http", auth="public", website=True)
    def self_service_profile(self, **kwargs):
        if request.session and request.session.uid:
            return request.render("g2p_self_service_portal.profile_page")

    @http.route(["/selfservice/aboutus"], type="http", auth="public", website=True)
    def self_service_about_us(self, **kwargs):
        return request.render("g2p_self_service_portal.aboutus_page")

    @http.route(["/selfservice/contactus"], type="http", auth="public", website=True)
    def self_service_contact_us(self, **kwargs):
        return request.render("g2p_self_service_portal.contact_us")

    @http.route(["/selfservice/staticpage"], type="http", auth="public", website=True)
    def self_service_static_page(self, **kwargs):
        return request.render("g2p_self_service_portal.static_page")

    @http.route(["/selfservice/errorpage"], type="http", auth="public", website=True)
    def self_service_error_page(self, **kwargs):
        return request.render("g2p_self_service_portal.error_page")

    @http.route(["/selfservice/home"], type="http", auth="user", website=True)
    def self_service_home(self, **kwargs):
        query = request.params.get("query")
        domain = [("name", "ilike", query)]

        programs = request.env["g2p.program"].sudo().search(domain).sorted("id")
        partner_id = request.env.user.partner_id
        states = {"draft": "Submitted", "enrolled": "Enrolled"}
        amount_received = 0
        myprograms = []
        for program in programs:
            membership = (
                request.env["g2p.program_membership"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            # date = datetime.strptime(membership['enrollment_date'], '%Y-%m-%d')
            # output_date = date.strftime('%d-%b-%Y')
            amount_issued = sum(
                ent.amount_issued
                for ent in request.env["g2p.payment"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            amount_received = sum(
                ent.amount_paid
                for ent in request.env["g2p.payment"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            if len(membership) > 0:
                myprograms.append(
                    {
                        "id": program.id,
                        "name": program.name,
                        "has_applied": len(membership) > 0,
                        "status": states.get(membership.state, "Error"),
                        "issued": "{:,.2f}".format(amount_issued),
                        "paid": "{:,.2f}".format(amount_received),
                        "enrollment_date": membership.enrollment_date.strftime(
                            "%d-%b-%Y"
                        )
                        if membership.enrollment_date
                        else None,
                        "is_latest": (datetime.today() - program.create_date).days < 21,
                        "application_id": membership.application_id
                        if membership.application_id
                        else None,
                    }
                )

        entitlement = sum(
            ent.amount_issued
            for ent in request.env["g2p.payment"]
            .sudo()
            .search([("partner_id", "=", partner_id.id)])
        )
        received = sum(
            ent.amount_paid
            for ent in request.env["g2p.payment"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", partner_id.id),
                ]
            )
        )
        pending = entitlement - received
        labels = ["Received", "Pending"]
        values = [received, pending]
        data = json.dumps({"labels": labels, "values": values})

        return request.render(
            "g2p_self_service_portal.dashboard",
            {"programs": myprograms, "data": data},
        )

    @http.route(["/selfservice/programs"], type="http", auth="user", website=True)
    def self_service_all_programs(self, page="1", limit="7", **kwargs):
        limit = int(limit)
        page = int(page)
        query = kwargs.get("q", "")
        domain = [("name", "ilike", query)]

        if page < 1:
            page = 1
        if limit < 5:
            limit = 5
        programs = (
            request.env["g2p.program"]
            .sudo()
            .search(domain, limit=limit, offset=(page - 1) * limit, order="id")
        )

        total = ceil(request.env["g2p.program"].sudo().search_count([]) / limit)

        partner_id = request.env.user.partner_id
        states = {"draft": "Submitted", "enrolled": "Enrolled"}

        values = []
        for program in programs:
            membership = (
                request.env["g2p.program_membership"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            values.append(
                {
                    "id": program.id,
                    "name": program.name,
                    "has_applied": len(membership) > 0,
                    "status": states.get(membership.state, "Error"),
                    "is_latest": (datetime.today() - program.create_date).days < 21,
                }
            )

        return request.render(
            "g2p_self_service_portal.allprograms",
            {
                "programs": values,
                "pager": {
                    "sel": page,
                    "total": total,
                },
            },
        )

    @http.route(
        ["/selfservice/apply/<int:_id>"], type="http", auth="user", website=True
    )
    def self_service_apply_programs(self, _id):
        program = request.env["g2p.program"].sudo().browse(_id)
        current_partner = request.env.user.partner_id

        for mem in current_partner.program_membership_ids:
            if mem.program_id.id == _id:
                return request.redirect(f"/selfservice/submitted/{_id}")

        view = program.self_service_portal_form.view_id

        return request.render(
            view.id,
            {
                "program": program.name,
                "program_id": program.id,
                "user": request.env.user.given_name,
            },
        )

    @http.route(
        ["/selfservice/submitted/<int:_id>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def self_service_form_details(self, _id, **kwargs):

        program = request.env["g2p.program"].sudo().browse(_id)
        current_partner = request.env.user.partner_id

        additional_info = (
            current_partner.additional_g2p_info
            if current_partner.additional_g2p_info
            else []
        )

        if request.httprequest.method == "POST":
            form_data = kwargs

            if isinstance(additional_info, list):
                already_present = False
                for element in additional_info:
                    if element["id"] == _id:
                        already_present = True
                        element["data"].update(form_data)
                        break
                if not already_present:
                    additional_info.append(
                        {"id": _id, "name": program.name, "data": form_data}
                    )
            elif isinstance(additional_info, dict):
                additional_info.update(form_data)
            else:
                _logger.error("Found Bad Additional G2P Info")

            current_partner.additional_g2p_info = additional_info

            apply_to_program = {
                "partner_id": current_partner.id,
                "program_id": program.id,
            }

            program_member = (
                request.env["g2p.program_membership"].sudo().create(apply_to_program)
            )

        else:
            program_member = (
                request.env["g2p.program_membership"]
                .sudo()
                .search(
                    [
                        ("program_id", "=", program.id),
                        ("partner_id", "=", current_partner.id),
                    ],
                    limit=1,
                )
            )

            if len(program_member) < 1:
                return request.redirect(f"/selfservice/apply/{_id}")

        form_arch_xml = ""
        try:
            form_arch_xml = ET.fromstring(
                program.self_service_portal_form.view_id.arch
            )[0][0]
            inputs = form_arch_xml.findall(".//input")
            addl_info_program = next(
                (prog["data"] for prog in additional_info if prog["id"] == _id), {}
            )
            for element in inputs:
                element.set("readonly", "1")
                element.set("value", addl_info_program.get(element.get("name"), ""))
            form_arch_xml = ET.tostring(form_arch_xml).decode()
        except Exception as e:
            _logger.error("Error Rendering the form", e)

        return request.render(
            "g2p_self_service_portal.self_service_form_submitted",
            {
                "program": program.name,
                "submission_date": program_member.enrollment_date,
                "application_id": program_member.application_id,
                "user": current_partner.given_name,
                "output_form": form_arch_xml if form_arch_xml else None,
            },
        )
