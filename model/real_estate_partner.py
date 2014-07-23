# -*- coding: utf-8 -*-
# #############################################################################
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


class dev_contact(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'

    _columns = {
        'country_id': fields.many2one('res.country', 'Nationality'),
        'national_identity_number': fields.integer('Unique national identity number', size=8),
        'national_identity_issue': fields.date('Date of issue', size=32),
        'national_identity_number_state': fields.many2one('res.country.state', 'place of issue', size=32),
        'gender': fields.selection([('male', 'Male'), ('female', 'Female')], 'Gender'),
        'marital': fields.selection([('single', 'Single'), ('married_sep', 'Married under the separate property'),
                                     ('married_join', 'married on the basis of joint ownership of property'),
                                     ('widower', 'Widower'), ('divorced', 'Divorced')], 'Marital situation '),
        'birthday': fields.date("Birthday date"),
        'parent_id_contacts': fields.many2one('res.partner', 'Related Company'),
        'child_contacts': fields.one2many('res.partner', 'parent_id_contacts', 'Spouse',
                                          domain=[('active', '=', True)]),


    }


dev_contact()








# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

