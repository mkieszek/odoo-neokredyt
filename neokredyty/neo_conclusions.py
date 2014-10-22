# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
import pdb
import datetime

class neo_conclusions(osv.Model):
    _name = 'neo.conclusions'
        
    _columns = {
            'file_data_conclusions': fields.binary('File', required=True),
            'partner_id' : fields.many2one('res.partner'),
            'description_conc' : fields.char('Opis'),
            'file_name': fields.char('File name', size=64),
    }