# -*- coding: utf-8 -*-
from openerp.osv.orm import Model
from openerp.osv import fields

class neo_schedule(Model):
    _name = "neo.schedule"
    _columns = {
        'name' : fields.char('Nr raty',readonly=True),
        'credit_id' : fields.many2one('neo.credit'),
        'repayment_interest' : fields.float('Odseteki',readonly=True),
        'repayment_credit' : fields.float('Kapitał',readonly=True),
        'full_installment' :fields.float('Pełna rata',readonly=True),
        'repay': fields.float('Pozostało do spłaty',readonly=True),
    }