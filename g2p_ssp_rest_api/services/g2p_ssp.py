from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_pydantic.restapi import PydanticModelList
from odoo.addons.component.core import Component

from ..models.program_membership import ProgramMembershipOut


class SSPApiService(Component):
    _inherit = "base.rest.service"
    _name = "g2p_ssp.rest.service"
    _usage = "program"
    _collection = "base.rest.ssp.services"
    _description = """
        Self Service Portal API Services
    """

    @restapi.method(
        [(["/memberships"], "GET")],
        output_param=PydanticModelList(ProgramMembershipOut),
        auth="user",
    )
    def get_program_memberships(self, limit: int = 80):
        partner_id = self.env.user.partner_id.id
        # TODO: Create Access Rights and Record Rules to limit access to Program Memberships for the current user
        program_memberships = self.env["g2p.program_membership"].sudo()
        prog_mem_search_res = program_memberships.search(
            [("partner_id", "=", partner_id)], limit=limit
        )
        program_mem_state_dict = dict(program_memberships._fields["state"].selection)
        res = []
        for p_mem in prog_mem_search_res:
            res.append(
                ProgramMembershipOut(
                    id=p_mem.id,
                    partner_id=p_mem.partner_id.id,
                    partner_name=p_mem.partner_id.name,
                    program_id=p_mem.program_id.id,
                    program_name=p_mem.program_id.name,
                    enrollment_date=p_mem.enrollment_date,
                    state=program_mem_state_dict.get(p_mem.state),
                )
            )
        return res
