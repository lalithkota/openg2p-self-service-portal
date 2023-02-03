from odoo.addons.base_rest.controllers import main


class RegistryApiController(main.RestController):
    _root_path = "/api/v1/ssp/"
    _collection_name = "base.rest.ssp.services"
    _default_auth = "user"
