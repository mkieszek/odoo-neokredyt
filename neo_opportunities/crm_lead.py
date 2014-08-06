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
    }