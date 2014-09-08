# -*- coding: utf-8 -*-
from openerp.osv.orm import Model
from openerp.osv import fields
from datetime import date

import pdb
import datetime

class neo_schedule(Model):
    _name = "neo.schedule"
    _columns = {
        'date_rate' : fields.date('Data        ',readonly=True),
        'credit_id' : fields.many2one('neo.credit',readonly=True),
        'repayment_interest' : fields.float('Odseteki',readonly=True),
        'repayment_credit' : fields.float('Kapitał',readonly=True),
        'full_installment' :fields.float('Pełna rata',readonly=True),
        'payment_day' : fields.date('Data zapłacenia'),
        'repay': fields.float('Pozostało do spłaty',readonly=True),
        'report_krd_big' : fields.integer('Raport KRD/BIG'),
        'payment_request' : fields.integer('Wezwania do zapłaty'),
        'delay_day' : fields.integer('opóźnienie (dni)',readonly=True),
    }
    
    
    def write(self, cr, uid, ids, vals, context=None):
        schedule = self.browse(cr, uid, ids)
        
        date_rate = datetime.datetime.strptime(schedule.date_rate,'%Y-%m-%d').date()
        payment_day = datetime.datetime.strptime(vals['payment_day'],'%Y-%m-%d').date()  
              
        if vals['payment_day']:
            delay_day = payment_day - date_rate
            data = {}
            data['delay_day'] = int(delay_day.days)
            data['payment_day'] = vals['payment_day']
            
        return super(neo_schedule, self).write(cr, uid, ids, data, context=context)