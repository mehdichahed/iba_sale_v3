# -*- coding: utf-8 -*-
# #############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
# This program is free software: you can redistribute it and/or modify
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


class facing_product(osv.osv):
    _name = 'facing.estate.product'
    _description = 'Facing product'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'description': fields.text('Description', translate=True),
        'active': fields.boolean('Active',
                                 help="If a facing is not active, it will not be displayed in the list of facing"),
    }
    _defaults = {
        'active': 1,
    }


facing_product()


class project(osv.osv):
    _name = 'project.estate.product'
    _description = 'project.estate.product'
    _columns = {
        'name': fields.char('Name', size=64),
        'description': fields.text('Description', translate=True),
        'active': fields.boolean('Active',
                                 help="If a project is not active, it will not be displayed in the list of project"),
        'member_ids': fields.many2many('res.users', 'sale_member_rel', 'section_id', 'member_id', 'Team Members'),
        'reply_to': fields.char('Reply-To', size=64,
                                help="The email address put in the 'Reply-To' of all emails sent by OpenERP about cases in this sales team"),
        'parent_id': fields.many2one('crm.case.section', 'Parent Team'),
        'child_ids': fields.one2many('crm.case.section', 'parent_id', 'Child Teams'),
    }
    _defaults = {
        'active': 1,
    }
    _constraints = [
        (osv.osv._check_recursion, 'Error ! You cannot create recursive Sales team.', ['parent_id'])
    ]


project()


class round(osv.osv):
    _name = 'round.estate.product'
    _columns = {
        'name': fields.char('Name', size=64),
        'description': fields.text('Description', translate=True),
        'active': fields.boolean('Active', help="If a round is not active, it will not be displayed in the project"),
    }
    _defaults = {
        'active': 1,
    }


round()


class property_type(osv.osv):
    _name = 'property.type.estate.product'
    _columns = {
        'name': fields.char('Name', size=64),
        'description': fields.text('Description', translate=True),
        'active': fields.boolean('Active',
                                 help="If a property type is not active, it will not be displayed in the project"),
    }
    _defaults = {
        'active': 1,
    }


property_type()


class room(osv.osv):
    _name = 'room.estate.product'
    _columns = {
        'name': fields.char('Name', size=64),
        'description': fields.text('Description', translate=True),
        'active': fields.boolean('Active', help="If a room is not active, it will not be displayed in apartment type"),
    }
    _defaults = {
        'active': 1,
    }


room()


class floor(osv.osv):
    _name = 'floor.estate.product'
    _columns = {
        'name': fields.char('Name', size=64),
        'description': fields.text('Description', translate=True),
        'active': fields.boolean('Active', help="If a floor is not active, it will not be displayed in the project"),
    }
    _defaults = {
        'active': 1,
    }


floor()


class dev_article_local(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'

    def _total_area(self, cr, uid, ids, name, args, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = (record.outside_work_area + record.common_area + record.covered_terrace)
        return res


    _columns = {
        'margin': fields.float('Margin', size=64, digits_compute=dp.get_precision('Product Price')),
        'outside_work_area': fields.float('Outside work area', size=64, required=True,
                                          digits_compute=dp.get_precision('Product Unit of Measure')),
        'common_area': fields.float('Common area', required=True, size=64,
                                    digits_compute=dp.get_precision('Product Unit of Measure')),
        'covered_terrace': fields.float('covered terrace', size=64,
                                        digits_compute=dp.get_precision('Product Unit of Measure')),
        'garden_area': fields.float('Surface jardin', size=64,
                                    digits_compute=dp.get_precision('Product Unit of Measure')),
        'total_area': fields.function(_total_area, string='Total area', store=True,
                                      digits_compute=dp.get_precision('Product Unit of Measure')),
        'list_price': fields.float('Prix de vente', digits_compute=dp.get_precision('Product Price'), required=True,
                                   help="Base price to compute the customer price. Sometimes called the catalog price."),
        'statut': fields.selection(
            [('new', 'New'), ('promised_to', 'Promised to'), ('sold_out', 'Sold out'), ('lost', 'Lost')],
            'Status of property', readonly=True),
        'type': fields.selection([('product', 'Marchandise'), ('consu', 'Consumable'), ('service', 'Service'),
                                  ('bien_immobilier', 'Bien immobilier')], 'Product Type', required=True,
                                 help="Consumable: Will not imply stock management for this product. \nStockable product: Will imply stock management for this product."),
        'floor': fields.many2one('floor.estate.product', 'floor'),
        'project': fields.many2one('project.estate.product', 'Project'),
        'round': fields.many2one('round.estate.product', 'Round'),
        'property_type': fields.many2one('property.type.estate.product', 'property type'),
        'facing_type': fields.many2one('facing.estate.product', 'Facing type'),
        'number_of_rooms': fields.many2one('room.estate.product', 'Facing type'),
    }
    _defaults = {
        'status': 'new'
    }


dev_article_local()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

