# -*- coding: utf-8 -*-
from openerp.osv.orm import Model
from openerp.osv import fields

class neo_schedule(Model):
    _name = "neo.schedule"
    _columns = {
        'name' : fields.char('Nazwa'),
        'credit_id' : fields.many2one('neo.credit'),
        'month' : fields.date('Miesiąc'),
        'start_balance' : fields.float('Saldo początkowe kapitału'),
        'repayment_interest' : fields.float('Spłata odsetek'),
        'repayment_credit' : fields.integer('Spłata kredytu'),
        'full_installment' :fields.float('Pełna rata'),
        'repay': fields.float('Pozostało do spłaty'),
    }