# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields, osv

AVAILABLE_STATES = [
    ('active', 'Aktywny'),
    ('closed', 'Zamknięty'),
    ('vindication', 'W windykacji'),
]

class neo_credit_stage(osv.Model):
     _name = 'neo.credit.stage'
     _columns = {
        'name': fields.char('Name', required=True),
        'sequence': fields.integer('Sequence', help="Used to order the note stages"),
        'state' : fields.selection(AVAILABLE_STATES, 'State', required=True),
     }