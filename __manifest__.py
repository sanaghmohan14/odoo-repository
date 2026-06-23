{
    'name': 'vechicle repair management',
    'version': '19.0.1.1',
    'author': "cybrosys",
    'category': "service",
    'sequence': -10,
    'summary': "This is a vechicle service management module",
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ["mail"],
    'data': ["security/ir.model.access.csv",
             "data/reference.xml",
             "data/demo.xml",
             "views/vehicle_tags.xml",
             "views/vechicle_views.xml",
             "views/vechicle_repair_menu.xml"]

}
