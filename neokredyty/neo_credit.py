# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields
import pdb
import neo_credit_stage



class neo_credit(Model):
    _name = "neo.credit"
    

    _columns = {
        'name' : fields.char('Nazwa',required=True),
        'schedule_ids' : fields.one2many('neo.schedule','credit_id'),
        'client_id': fields.many2one('res.partner', 'Klient',required=True),
        'telephone' : fields.integer('Nr kontaktowy'),
        'address' : fields.char('Adres korespondencyjny'),
        'email' : fields.char('Mail'),
        'product_id' :fields.many2one('product.product', 'Produkt'),
        'contract_date' :fields.date('Data umowy'),
        'commission' : fields.float('Prowizja'),
        'interest' : fields.float('Oprocentowanie'),
        'period' : fields.integer('Okres'),
        'end_date' : fields.date('Data zakończenia umowy'),
        'insurance' : fields.char('Ubezpieczenie'),
        'year': fields.integer('Rok'),
        'months': fields.integer('Miesiąc'),
        'day' : fields.integer('Dzień raty'),
        'delay_day' : fields.integer('Ilość dni opóźnienia'),
        'payment_request' : fields.integer('Wezwania do zapłaty'),
        'report_krd_big' : fields.integer('Raport KRD/BIG'),
        'termination' : fields.selection((('1','TAK'),('2','NIE')), 'Wypowiedzenie umowy'),
        'charge_call' : fields.float('Opłata za wezwanie'),
        'installment' : fields.float('Rata',readonly=True),
        'total_arrears' : fields.float('Suma zaległości'),
        'amount_insurance' : fields.float('Kwota ubezpieczenia'),
        'amount_credit' : fields.float('Kwota kredytu'),
        'total_liabilities' : fields.float('Suma zobowiązania',readonly=True),
        'stage_id' : fields.many2one('neo.credit.stage','Status'),
        'type_schedule' : fields.selection((('1','Raty malejące'),('2','Raty równe')), 'Raty'),
    }
    
    
    def create(self, cr, uid, data, context=None):
        
        credit_id = super(neo_credit, self).create(cr, uid, data, context=context)
        credit = self.browse(cr, uid, credit_id)
                
        total_liabilities = credit.amount_credit + credit.amount_insurance
        
        vals_credit = {}
        vals_credit['total_liabilities'] = total_liabilities
        
        self.write(cr, uid, [credit_id], vals_credit)
        
        schedule_obj = self.pool.get('neo.schedule')
        
        dosplaty = total_liabilities
        
        vals_schedule = {}
        vals_schedule['credit_id'] = credit_id
        rata = total_liabilities / credit.period
        rata2 = total_liabilities*(q**credit.period)*(q-1)/((q**credit.period)-1) 
        q=1+((0.0833333333)*(credit.interest/100))
        
        
        i=0
        pdb.set_trace()
        if credit.type_schedule == '1':
            while i < credit.period:
                odsetki = dosplaty * credit.interest/100/12
                dosplaty = dosplaty - rata
                vals_schedule['repayment_interest'] = odsetki
                vals_schedule['repay'] = dosplaty
                vals_schedule['full_installment'] = rata + odsetki
                vals_schedule['repayment_credit'] = rata
                vals_schedule['name'] = i+1
                schedule_obj.create(cr, uid, vals_schedule)
                i += 1
        elif credit.type_schedule == '2':
            while i < credit.period:
                odsetki = (q-1)*dosplaty
                kapital = 0.0
                kapital = rata - odsetki
                dosplaty = dosplaty - kapital
                vals_schedule['repayment_interest'] = odsetki
                vals_schedule['repayment_credit'] = kapital
                vals_schedule['repay'] = dosplaty
                vals_schedule['full_installment'] = rata
                vals_schedule['name'] = i+1
                schedule_obj.create(cr, uid, vals_schedule)
                i += 1
        return credit_id
    