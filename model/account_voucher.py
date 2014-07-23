#-*- coding: utf-8 -*-

__author__ = 'Samir'

from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_voucher(osv.osv):
    _name = 'account.voucher'
    _inherit = 'account.voucher'

    def onchange_purchaseorder(self, cr, uid, ids, purchaseord, context=None):
        if purchaseord:
            partner_id = self.pool.get('sale.order').browse(cr, uid,purchaseord , context).partner_id.id
            return {'value':{'partner_id':partner_id}}
        return {}

    def _sending_mail_to_change_state(self,cr ,uid ,ids , user_id, purchaseord, context=None):

        user_mail = user_id.email
        #recupere les utilisateurs du groupe .
        dir_general_groups_ids = self.pool.get('res.groups').search(cr, uid , [ ('name', '=', 'Service financier')])[0]
        groupe  = self.pool.get('res.groups').browse(cr, uid , dir_general_groups_ids)
        groupe_mail = ''
        for utilisateur in groupe.users :
            if (utilisateur.email) :
                groupe_mail += utilisateur.email+','

        if(self.pool.get('res.company').browse(cr, uid , 1).email):

            ir_mail_server = self.pool.get('ir.mail_server')

            company_mail = self.pool.get('res.company').browse(cr, uid , 1).name + "<" + self.pool.get('res.company').browse(cr, uid , 1).email + ">"
            #get template .
            template_obj = self.pool.get('email.template')
            template_id = self.pool.get('email.template').search(cr, uid , [('name', '=', 'promised')])[0]
            if(template_id):
                template = self.pool.get('email.template').browse(cr, uid , template_id)
                msg = ir_mail_server.build_email(company_mail, [user_mail,groupe_mail], template.subject, template.body_html ,subtype='Paid')
            else:
                subject = 'Mise a jour du statut de votre bien'
                message = ' le message inclut au bout du code python'
                msg = ir_mail_server.build_email(company_mail, [user_mail,groupe_mail], subject,message )
            body = template_obj.render_template(cr, uid , template.body_html , template.model_id.model ,ids[0])
            msg = ir_mail_server.build_email(company_mail, [user_mail,groupe_mail], template.subject, body )
            ir_mail_server.send_email(cr, uid, msg)
        #self.message_post(cr, uid, 0, _('My subject'),_("has received a <b>notification</b> and is happy for it."), context=context)
        return True


    def _change_product_statut(self, cr, uid, ids ,context=None):
        b_cmd = self.browse(cr,uid,ids,context)[0].bon_commande_id
        # tester sur le montant
        total_commande = b_cmd.amount_total
        id_pre_payement = self.pool.get('account.voucher').search(cr, uid , [ ('bon_commande_id', '=', b_cmd.id) ], context=context)
        total_accompte = 0
        for accompte_id in id_pre_payement:
            acc_pay_obj = self.pool.get('account.voucher').browse(cr,uid, accompte_id)
            total_accompte += acc_pay_obj.amount

        if(total_accompte > total_commande):
            raise osv.except_osv("l'operation ne peut pas s'effectuer",'vous avez depasse le montant du bien ')
        #modifier statut des produits.
        if(total_accompte > 0):
            prod_cmd = b_cmd.order_line
            if(len(prod_cmd) > 1):
                iiterator = (0,len(prod_cmd)-1)
            else :
                iiterator = {0}
            for i in iiterator:
                vals = {'statut' : 'promised' }
                bien_immobilier = self.browse(cr,uid,ids,context)[0].bon_commande_id.order_line[0].product_id
                statut_actuelle = bien_immobilier.statut
                if((statut_actuelle == 'new') and (bien_immobilier.type == 'bien_immobilier')):
                    id_produit = self.browse(cr,uid,ids,context)[0].bon_commande_id.order_line[0].product_id
                    self.pool.get('product.product').write(cr,uid, id_produit.id, vals)

                    #sending mail notifications.
                    try:
                        self._sending_mail_to_change_state(cr ,uid ,ids,b_cmd.partner_id ,id_produit)
                    except :
                        print("mail failed")


    def proforma_voucher(self, cr, uid, ids, context=None):
        self.action_move_line_create(cr, uid, ids, context=context)
        if( self.browse(cr,uid , ids)[0].use_prepayment_account ):
            self._change_product_statut(cr,uid, ids, context=context)
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account_voucher.tn',
            'datas': datas,
            'nodestroy' : True
        }

    _columns = {

        'bon_commande_id': fields.many2one('sale.order', 'Purchase order'),

    }



account_voucher()

#à utiliser juste pour le fichier ir.acess
class account_voucher_line(osv.osv):
    _name = 'account.voucher.line'
    _inherit = 'account.voucher.line'
account_voucher_line()

class account_period(osv.osv):
    _name = 'account.period'
    _inherit = 'account.period'
account_period()

class account_move_reconcile(osv.osv):
    _name = 'account.move.reconcile'
    _inherit = 'account.move.reconcile'
account_move_reconcile()

class account_move(osv.osv):
    _name = 'account.move'
    _inherit = 'account.move'
account_move()

class account_move_line(osv.osv):
    _name = 'account.move.line'
    _inherit = 'account.move.line'
account_move_line()

class account_analytic_line(osv.osv):
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'
account_analytic_line()

class res_country(osv.osv):
    _name = 'res.country'
    _inherit = 'res.country'
res_country()
