__author__ = 'sa.guesmi'

from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    def print_client_doc(self, cr, uid,ids ,context=None ):
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return{
            'type': 'ir.actions.report.xml',
            'report_name': 'account.sheet.customer',
            'datas': datas,
            'nodestroy' : True
        }

account_invoice()