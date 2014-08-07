# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    _description = "Szansa"
    _columns = {
        'adviser': fields.char('Doradca'),
        'adv_mail': fields.char('Mail'),
        'adv_tel': fields.char('Tel.'),
        'payment_date' : fields.datetime('Data wypłaty'),
        'amount' : fields.float('Kwota'),
        'bank' : fields.char('Bank'),
        'interest' : fields.float('Oprocentowanie'),
        'bank_comission' : fields.char('Prowizja banku'),
        'period' : fields.integer('Okres'),
        'installment' : fields.float('Rata'),
        'insurance' : fields.float('Kwota ubezpieczeniowa'),
        'insurer' : fields.char('Ubezpieczyciel'),
        'rrso' : fields.float('RRSO'),
        'commission' : fields.integer('Prowizja za wcześniejszą spłatę'),
        'number_queries' : fields.integer('Ilość zapytań przez Neokredyt')
    }