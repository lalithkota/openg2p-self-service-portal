from odoo.addons.base_rest.controllers import main


class RegistryApiController(main.RestController):
    _root_path = "/api/v1/selfservice/"
    _collection_name = "base.rest.self.service.services"
    _default_auth = "user"
