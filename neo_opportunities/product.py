# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields

class product_product(Model):
    _inherit = "product.product"
    _columns = {
        'type_client': fields.boolean('Klient indywidualny'),
    }