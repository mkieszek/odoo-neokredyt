# -*- coding: utf-8 -*-
import pdb
import neo_credit_stage
import datetime
import time

from openerp.osv.orm import Model
from openerp.osv import fields
from datetime import date
from dateutil.relativedelta import relativedelta

class neo_credit(Model):
    _name = "neo.credit"
    
    def _contract_month(self, cr, uid, ids, data, arg, context=None):
        vals = {}
        
        for credit in self.browse(cr, uid, ids):
            if credit.contract_date:
                c_date = datetime.datetime.strptime(credit.contract_date,"%Y-%m-%d").date()
                vals[credit.id] = str(c_date.month).zfill(2)
        return vals
    
    def _contract_year(self, cr, uid, ids, data, arg, context=None):
        vals = {}
        
        for credit in self.browse(cr, uid, ids):
            if credit.contract_date:
                #pdb.set_trace()
                con_date = datetime.datetime.strptime(credit.contract_date,"%Y-%m-%d").date()
                vals[credit.id] = str(con_date.year).zfill(2)
        return vals

    def _end_month(self, cr, uid, ids, data, arg, context=None):
        vals = {}
        
        for credit in self.browse(cr, uid, ids):
            if credit.end_date:
                e_date = datetime.datetime.strptime(credit.end_date,"%Y-%m-%d").date()
                vals[credit.id] = str(e_date.month).zfill(2)
        return vals

        
    _columns = {
        'name' : fields.char('Nazwa',required=True, readonly=True, select=True),
        'schedule_ids' : fields.one2many('neo.schedule','credit_id'),
        'client_id': fields.many2one('res.partner', 'Klient', required=True),
        'phone' : fields.related('client_id', 'phone', type='char', string='Telefon', readonly=True),
        'mobile' : fields.related('client_id', 'mobile', type='char', string='Telefon kom.', readonly=True),
        'address' : fields.related('client_id', 'contact_address', type='char', string='Adres', readonly=True),
        'email': fields.related('client_id', 'email', type='char', string='Email', readonly=True),
        'product_id' :fields.many2one('product.product', 'Produkt',required=True),
        'contract_date' :fields.date('Data umowy',required=True),
        'contract_date_month' : fields.function(_contract_month, string="Miesiąc wypłaty", type='char', store=True),
        'contract_date_year' : fields.function(_contract_year, string="rok", type='char', store=True),
        'commission' : fields.float('Prowizja'),
        'interest' : fields.float('Oprocentowanie',required=True),
        'period' : fields.integer('Okres (miesiące)',required=True),
        'end_date' : fields.date('Data zakończenia umowy', readonly=True),
        'end_date_month' : fields.function(_end_month, string="Miesiąc zakończemia umowy", type='char', store=True),
        'insurance' : fields.char('Ubezpieczenie'),
        'amount_insurance' : fields.float('Kwota ubezpieczenia'),
        'amount_credit' : fields.float('Kwota kredytu',required=True),
        'stage_id' : fields.many2one('neo.credit.stage','Status'),
        'day_rate' : fields.integer('Dzień raty',required=True),
        'type_credit' : fields.selection((('1','Raty malejące'),('2','Raty równe')), 'Raty',required=True),
        'sum_interest' : fields.float('Suma odsetek', readonly=True),
        'sum_credit' : fields.float('Całkowity koszt kredytu', readonly=True),
        
    }
    _defaults = {
        'name': lambda obj, cr, uid, context: '.'}
    
    def create(self, cr, uid, data, context=None):
        
        if data.get('name','.')=='.':
            data['name'] = self.pool.get('ir.sequence').get(cr, uid, 'neo.credit') or '.'
        
        stage_id = self.pool.get('neo.credit.stage').search(cr, uid, [('sequence','=',10)])[0]
        data['stage_id'] = stage_id
        credit_id = super(neo_credit, self).create(cr, uid, data, context=context)
        credit = self.browse(cr, uid, credit_id)
        
        total_liabilities = credit.amount_credit + credit.amount_insurance
        contract_date = datetime.datetime.strptime(data['contract_date'],'%Y-%m-%d').date()
        end_date = contract_date + relativedelta(months=credit.period)
        date_rate = contract_date + relativedelta(day=credit.day_rate)
        
        vals_credit = {}
        vals_credit['total_liabilities'] = total_liabilities
        vals_credit['end_date'] = end_date
        self.write(cr, uid, [credit_id], vals_credit)
        
        self.create_schedule(cr, uid, credit_id, False, context)
        return credit_id
    
    def create_schedule(self, cr, uid, credit_id, vals_sched=False, context=None):
        sum_interest = 0.0
        sum_credit = 0.0
        
        credit = self.browse(cr, uid, credit_id)
        total_liabilities = credit.amount_credit + credit.amount_insurance
        contract_date = datetime.datetime.strptime(credit.contract_date,'%Y-%m-%d').date()
        end_date = contract_date + relativedelta(months=credit.period)
        date_rate = contract_date + relativedelta(day=credit.day_rate)
        
        schedule_obj = self.pool.get('neo.schedule')
         
        dosplaty = total_liabilities
        rata = total_liabilities / credit.period
        q=1+((0.0833333333)*(credit.interest/100))
        rata2 = total_liabilities*(q**credit.period)*(q-1)/((q**credit.period)-1)
        vals_schedule = {}
        vals_schedule['credit_id'] = credit_id
        i=0
        
        today = datetime.date.today()
        if credit.type_credit == '1':
            while i < credit.period:
                odsetki = dosplaty * credit.interest/100/12
                dosplaty = dosplaty - rata
                vals_schedule['repayment_interest'] = round(odsetki, 2)
                vals_schedule['repay'] = round(dosplaty, 2)
                vals_schedule['full_installment'] = round(rata, 2) + round(odsetki, 2)
                vals_schedule['repayment_credit'] = round(rata, 2)
                
                if vals_sched != False:
                    try:
                        vals_schedule['payment_day'] = vals_sched[i][0]
                        vals_schedule['payment_request'] = vals_sched[i][1]
                        vals_schedule['report_krd_big'] = vals_sched[i][2]
                    except:
                        pass
                
                sum_interest = sum_interest + odsetki
                sum_credit = sum_credit + rata
                
                if date_rate < contract_date:
                    date_rate = date_rate + relativedelta(months=1)
                vals_schedule['date_rate'] = date_rate
                date_rate = date_rate + relativedelta(months=1) + relativedelta(day=credit.day_rate)
                
                vals_schedule['sum_interest'] = sum_interest 
                vals_schedule['sum_credit'] = sum_credit + sum_interest
                schedule_obj.create(cr, uid, vals_schedule)
                self.write(cr, uid, [credit_id], vals_schedule)
                i += 1
                
                
        elif credit.type_credit == '2':
            while i < credit.period:
                odsetki = (q-1)*dosplaty
                kapital = 0.0
                kapital = rata2 - odsetki
                dosplaty = dosplaty - kapital
                vals_schedule['repayment_interest'] = round(odsetki, 2)
                vals_schedule['repayment_credit'] = round(kapital, 2)
                vals_schedule['repay'] = round(dosplaty, 2)
                vals_schedule['full_installment'] = round(kapital, 2) + round(odsetki, 2)
                
                if vals_sched != False:
                    try:
                        vals_schedule['payment_day'] = vals_sched[i][0]
                        vals_schedule['payment_request'] = vals_sched[i][1]
                        vals_schedule['report_krd_big'] = vals_sched[i][2]
                    except:
                        pass
                
                sum_interest = sum_interest + round(odsetki, 2)
                sum_credit = sum_credit + (round(kapital, 2) + round(odsetki, 2))
                
                if date_rate < contract_date:
                    date_rate = date_rate + relativedelta(months=1)
                vals_schedule['date_rate'] = date_rate
                date_rate = date_rate + relativedelta(months=1) + relativedelta(day=credit.day_rate)
                
                vals_schedule['sum_interest'] = sum_interest  
                vals_schedule['sum_credit'] = sum_credit            
                schedule_obj.create(cr, uid, vals_schedule)
                self.write(cr, uid, [credit_id], vals_schedule)
                i += 1
        return True


    def on_change_client_id(self, cr, uid, ids, client_id, context=None):
        values = {}
        if client_id:
            client = self.pool.get('res.partner').browse(cr, uid, client_id, context=context)
            values = {
                'phone': client.phone,
                'mobile': client.mobile,
                'address': client.contact_address,
                'email': client.email,

            }
        return {'value': values}
    
    def refresh_schedule(self, cr, uid, ids, data, context=None):
        vals={}
        for credit in self.browse(cr, uid, ids):
            vals_schedule={}
            l=0
            for schedule in credit.schedule_ids:
                vals_schedule[l] = [schedule.payment_day, schedule.payment_request, schedule.report_krd_big]
                l=l+1
                
            self.pool.get('neo.schedule').unlink(cr, uid, credit.schedule_ids.ids)
            
            self.create_schedule(cr, uid, credit.id, vals_schedule, context)
            
        return vals
    
    