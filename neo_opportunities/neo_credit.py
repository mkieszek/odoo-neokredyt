# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields

class neo_credit(Model):
    _name = "neo.credit"
    _columns = {
        'name' : fields.char('Nazwa'),
        'client_id': fields.many2one('res.partner', 'Klient'),
        'telephone' : fields.integer('Nr kontaktowy'),
        'address' : fields.char('Adres korespondencyjny'),
        'email' : fields.char('Mail'),
        'product_id' :fields.many2one('product.product', 'Produkt', domain="[('type_client','=',client_id.is_company)]"),
        'contract_date' :fields.datetime('Data umowy'),
        'commission' : fields.float('Prowizja'),
        'interest' : fields.float('Oprocentowanie'),
        'period' : fields.integer('Okres'),
        'end_date' : fields.datetime('Data zakończenia umowy'),
        'insurance' : fields.char('Ubezpieczenie'),
        'year': fields.selection([('2012','2012'),('2013','2013'),('2014','2014'),('2015','2015'),('2016','2016'),('2017','2017'),
                              ('2018','2018'),('2019','2019'),('2020','2020'),('2021','2021'),('2022','2022'),('2023','2023')],'Year'),
        'months': fields.selection([('1','January'),('2','February'),('3','March'),('4','April'),
                                ('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),
                                ('10','October'),('11','November'),('12','December')],'Month'),
        'day_installment' : fields.integer('Dzień raty'),
        'delay_day' : fields.integer('Ilość dni opóźnienia'),
        'payment_request' : fields.integer('Wezwania do zapłaty'),
        'report_krd_big' : fields.integer('Raport KRD/BIG'),
        'termination' : fields.selection((('1','TAK'),('2','NIE')), 'Wypowiedzenie umowy'),
        'charge_call' : fields.float('Opłata za wezwanie'),
        'installment' : fields.float('Rata'),
        'total_arrears' : fields.float('Suma zaległości'),
        'amount_insurance' : fields.float('Kwota ubezpieczenia'),
        'amount_credit' : fields.float('Kwota kredytu'),
        'total_liabilities' : fields.float('Suma zobowiązania'),
        
        
    }