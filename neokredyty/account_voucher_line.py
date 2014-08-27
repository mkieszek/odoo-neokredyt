# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields, osv
import pdb

AVAILABLE_MEASURE = [
    ('sztuka', 'szt.'),
    ('opakowanie', 'opk.'),
    ('skrzynia', 'skrz.')]

class account_voucher_line(osv.Model):
    _inherit = "account.voucher.line"
    _columns = {
        'quantity' : fields.integer('Ilość'),
        'measure' : fields.selection(AVAILABLE_MEASURE, 'Jednostka'), 
        'gross_amount' : fields.float('Cena jedn. brutto'),
     }
    
    def create(self, cr, uid, data, context=None):
        
        data['amount'] = data['quantity'] * data['gross_amount']
        account_id = super(account_voucher_line, self).create(cr, uid, data, context=context)        
        return account_id
   
   
    def write(self, cr, uid, ids, data, context=None):
        
        voucher = self.browse(cr, uid, ids)[0]
        
        if 'quantity' in data:
            qty = data['quantity']
        else:
            qty = voucher.quantity
            
        if 'gross_amount' in data:
            gross = data['gross_amount']
        else:
            gross = voucher.gross_amount
            
        data['amount'] = qty * gross
        account_id = super(account_voucher_line, self).write(cr, uid, ids, data, context=context)
        
        return account_id