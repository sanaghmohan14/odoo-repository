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
    'depends': ["mail", "contacts",'account','product','fleet'],
    'data': ["security/ir.model.access.csv",
             "wizards/create_vechicle_service.xml",
             "data/labor_product.xml",
             "views/res_partner_views.xml",
             "data/reference.xml",
             "data/demo.xml",
             "views/vehicle_tags.xml",
             "views/vechicle_views.xml",
             "views/vechicle_repair_menu.xml"]

}
