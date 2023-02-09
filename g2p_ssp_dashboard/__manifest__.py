{
    "name": "G2P Self Service Portal: Dashboard",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://github.com/OpenG2P/openg2p-self-service-portal",
    "license": "Other OSI approved licence",
    "development_status": "Production/Stable",
    "depends": ["g2p_self_service_base"],
    "data": [
        "templates/dashboard.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "g2p_self_service_dashboard/static/src/js/get_program_memberships.js",
        ],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
