# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
import pdb
import datetime

class neo_procedures(osv.Model):
    _name = 'neo.procedures'
        
    _columns = {
            'file_data_procedures': fields.binary('File', required=True),
            'partner_id' : fields.many2one('res.partner'),
            'description_proc' :fields.char('Opis'),
            'filename': fields.char('File name', size=64),
    }
            
    _defaults = {
                 'filename': 'defoult_name',
    }