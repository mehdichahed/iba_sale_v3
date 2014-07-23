# -*- coding: utf-8 -*-
# #############################################################################
# DEVCOSTKILLER *********************** Inc
# #############################################################################
{
    'name': 'sale IBA',
    'version': '1.1',
    'author': 'DevCostKILLER Tunisia',
    'category': '',
    'depends': [
        'sale', 'purchase', 'crm', 'hr', 'account_prepayment',
    ],
    'data': [
        'data/departement_data.xml', 'data/category_data.xml', 'data/groups.xml', 'data/company_data.xml',
        #'data/partner_employees_data.xml', 'data/users_data.xml', 'data/real_estate_product_data.xml',
        #'view/real_estate_menuitem.xml', 'view/real_estate_views.xml', 'view/real_estate_config_product_views.xml','workflow/real_estate_sale_workflow.xml',
        'view/real_estate_partner_view.xml',
        'view/real_estate_product_view.xml',
        'view/iba_addons_piste.xml',
        'workflow/sale_view.xml', 'workflow/workflow_approve_sale.xml',
        'notification/real_estate_email_template.xml',
        'view/real_estate_account_voucher_view.xml',
        'view/real_estate_agreement_to_sell.xml',
    ],

    'css': ["static/src/css/reservation.css"],
    'installable': True,
    'auto_install': False,


}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
