# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields

class res_partner(Model):
    _inherit = "res.partner"

    _columns = {
        'bank': fields.boolean('Bank', help="Check this box if this contact is a Bank."),
        'chances_ids' : fields.one2many('crm.lead','partner_id','Szanse'),
    }