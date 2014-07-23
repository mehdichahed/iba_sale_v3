# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class percentage_promised(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'

   # def ammount_compare (self, cr, uid, ids, context=None):
      #  percentage_of_promise = self.browse(cr , uid , ids[0],context=context).percentage_of_promise
      #  credit = self.browse(cr , uid , ids[0],context=context).credit
       # amount_untaxed = self.browse(cr , uid , ids[0],context=context).amount_untaxed
       # amount_untaxed = self.browse(cr , uid , ids[0],context=context).amount_untaxed

       # per = (amount_untaxed * percentage_of_promise)/100
       # if credit >=  per:




    def _check_percentage(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.percentage_of_promise < 0.0 or obj.percentage_of_promise > 100.0:
            return False
        return True

    _columns = {

        'percentage_of_promise': fields.float('Percentage of promise (%)', size=64, digits_compute=dp.get_precision('Account')),

    }

    _constraints = [
        (_check_percentage, 'the percentage entered must be between 0 and 100 ', ['percentage_of_promise']),

    ]
percentage_promised()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

