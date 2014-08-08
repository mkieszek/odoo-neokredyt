# -*- coding: utf-8 -*-
from openerp.osv.orm import Model
from openerp.osv import fields

class neo_schedule(Model):
    _name = "neo.schedule"
    _columns = {
        'name' : fields.char('Nazwa'),
        'credit_id' : fields.many2one('neo.credit'),
        'end_date' : fields.date('Data'),
        'part_interest' : fields.float('Część Odsetkowa'),
        'part_capital' : fields.float('Część kapitałowa'),
        'number_rate' : fields.integer('Numer raty'),
        'installment_all' :fields.float('Rata łącznie'),
        'capital_pay': fields.float('Kapitał do spłaty'),
    }