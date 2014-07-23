# -*- coding: utf-8 -*-
##############################################################################
#  DEVCOSTKILLER
##############################################################################

import time
from openerp.report import report_sxw
from openerp.tools import french_number
from openerp.tools.translate import _

class report_print_check(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_print_check, self).__init__(cr, uid, name, context)
        self.number_lines = 0
        self.number_add = 0
        self.localcontext.update({
            'time': time,
            'get_lines': self.get_lines,
            'fill_stars' : self.fill_stars,
            'client_account' : self.client_account,
            'statut_marital' : self.statut_marital,
            'project_name' : self.project_name,
        })
    def fill_stars(self, amount):
        amount = amount.replace('Dollars','')
        if len(amount) < 100:
            stars = 100 - len(amount)
            return ' '.join([amount,'*'*stars])

        else: return amount
    
    def get_lines(self, voucher_lines):
        result = []
        self.number_lines = len(voucher_lines)
        for i in range(0, min(10,self.number_lines)):
            if i < self.number_lines:
                res = {
                    'date_due' : voucher_lines[i].date_due,
                    'name' : voucher_lines[i].name,
                    'amount_original' : voucher_lines[i].amount_original and voucher_lines[i].amount_original or False,
                    'amount_unreconciled' : voucher_lines[i].amount_unreconciled and voucher_lines[i].amount_unreconciled or False,
                    'amount' : voucher_lines[i].amount and voucher_lines[i].amount or False,
                }
            else :
                res = {
                    'date_due' : False,
                    'name' : False,
                    'amount_original' : False,
                    'amount_due' : False,
                    'amount' : False,
                }
            result.append(res)
        return result

    def client_account(self,purchaseord_ref):
        purchaseord_ids = self.pool.get('sale.order').search(self.cr,self.uid,[('name','=',purchaseord_ref)])
        if len(purchaseord_ids) > 0 :
            bon_commande = self.pool.get('sale.order').browse(self.cr,self.uid,purchaseord_ids[0])
            prepayement_ids = self.pool.get('account.voucher').search(self.cr,self.uid,[('bon_commande_id','=',bon_commande.id)])
            if len(prepayement_ids) > 0 :
                total_account = 0
                for prepayement_id in prepayement_ids:
                    total_account = total_account + self.pool.get('account.voucher').browse(self.cr,self.uid,prepayement_id).amount
                return total_account
        return ''

    def statut_marital(self,marital):
        if marital == 'single':
            return 'Single'
        elif marital == 'married_sep':
            return 'Married under the separate property'
        elif marital == 'married_join':
            return 'married on the basis of joint ownership of property'
        elif marital == 'widower':
            return 'Widower'
        else :
            return 'Divorced'

    def project_name(self,project_name):
        if project_name == 'cascades':
            return 'Les Cascades'
        elif project_name == 'phoenix':
            return 'Phoenix'
        elif project_name == 'tej_el_molk':
            return 'Tej El Molk'
        elif project_name == 'sables_argentees':
            return 'Les Sables Argentees'
        else :
            return 'Jinene Beni Khiar'

report_sxw.report_sxw(
    'report.account.customer.sheet',
    'account.invoice',
    'addons/iba_sale_v3/report/check_print_top.mako',
    parser=report_print_check
)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
