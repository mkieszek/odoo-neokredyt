# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

import pdb
import datetime

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    _description = "Szansa"
    
    
    def _payment_month(self, cr, uid, ids, data, arg, context=None):
        vals = {}
        for lead in self.browse(cr, uid, ids):
            p_date = datetime.datetime.strptime(lead.payment_date,"%Y-%m-%d").date()
            vals[lead.id] = str(p_date.month).zfill(2)
        return vals
    
    def _payment_month_search(self, cr, uid, ids, data, arg, context=None):
        args_payment_month = []
        for cond in arg:
            args_payment_month.append(('payment_date_month',cond[1],cond[2]))
        
        lead_ids = self.search(cr, uid, args_payment_month, context=context)
        
        return [('id', 'in', lead_ids)]
    
    _columns = {
        'adviser': fields.char('Doradca'),
        'adv_mail': fields.char('Mail'),
        'adv_tel': fields.char('Tel.'),
        'payment_date' : fields.date('Data wypłaty'),
        'payment_date_month' : fields.function(_payment_month, string="Miesiąc wypłaty", type='char', store=True),
        'payment_month_search': fields.function(_payment_month_search, type="one2many", relation="crm.lead", string="Miesiąc wypłaty", fnct_search=_payment_month_search),
        'amount' : fields.float('Kwota'),
        'bank_id' : fields.many2one('res.partner', 'Bank', domain=[('bank','=','True')]),
        'product_id' : fields.many2one('product.product', 'Produkt'),
        'interest' : fields.float('Oprocentowanie'),
        'bank_comission' : fields.float('Prowizja banku'),
        'period' : fields.integer('Okres'),
        'rate' : fields.float('Rata'),
        'insurance' : fields.float('Kwota ubezpieczeniowa'),
        'insurer' : fields.char('Ubezpieczyciel'),
        'rrso' : fields.float('RRSO'),
        'commission' : fields.float('Prowizja za wcześniejszą spłatę'),
        'number_queries' : fields.integer('Ilość zapytań przez Neokredyt')
    }
    
    
