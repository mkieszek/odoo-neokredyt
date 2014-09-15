# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

import pdb
import datetime

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    _description = "Szansa"
    
    
    def _payment_month(self, cr, uid, ids, data, arg, context=None):
        vals = {}
        
        for lead in self.browse(cr, uid, ids):
            if lead.payment_date:
                p_date = datetime.datetime.strptime(lead.payment_date,"%Y-%m-%d").date()
                vals[lead.id] = str(p_date.month).zfill(2)
        return vals
    
    def _payment_month_search(self, cr, uid, ids, data, arg, context=None):
        args_payment_month = []
        for cond in arg:
            args_payment_month.append(('payment_date_month',cond[1],cond[2]))
        
        lead_ids = self.search(cr, uid, args_payment_month, context=context)
        
        return [('id', 'in', lead_ids)]
    
    _columns = {
        'adviser': fields.char('Doradca'),
        'adv_mail': fields.char('Mail'),
        'adv_tel': fields.char('Tel.'),
        'payment_date' : fields.date('Data wypłaty'),
        'payment_date_month' : fields.function(_payment_month, string="Miesiąc wypłaty", type='char', store=True),
        'payment_month_search': fields.function(_payment_month_search, type="one2many", relation="crm.lead", string="Miesiąc wypłaty", fnct_search=_payment_month_search),
        'amount' : fields.float('Kwota'),
        'bank_id' : fields.many2one('res.partner', 'Bank', domain=[('bank','=','True')]),
        'product_id' : fields.many2one('product.product', 'Produkt'),
        'interest' : fields.float('Oprocentowanie'),
        'bank_comission' : fields.float('Prowizja banku'),
        'period' : fields.integer('Okres'),
        'rate' : fields.float('Rata'),
        'insurance' : fields.float('Kwota ubezpieczeniowa'),
        'insurer' : fields.char('Ubezpieczyciel'),
        'rrso' : fields.float('RRSO'),
        'commission' : fields.float('Prowizja za wcześniejszą spłatę'),
        'number_queries' : fields.integer('Ilość zapytań przez Neokredyt')
    }
    
    def create(self, cr, uid, data, context=None):
        
        lead_id = super(crm_lead, self).create(cr, uid, data, context=context)
        self.send_mail(cr, uid, lead_id, context)
        return lead_id
    
    def send_mail(self, cr, uid, lead_id, context=None):
        #pdb.set_trace()
        users_obj = self.pool.get('res.users')
        user = users_obj.browse(cr, uid, uid)
        lead = self.browse(cr, uid, lead_id)
        
        mail_to = ""
        if lead.user_id.partner_id.email is not False and lead.user_id.active is True:
            mail_to += lead.user_id.partner_id.email 
        if mail_to is not "":
            url = ("http://192.168.56.10:8069/?db=%s#id=%s&view_type=form&model=crm.lead")%(cr.dbname, lead_id)
            pdb.set_trace()
            subject = ("Zostałeś dodany do nowo utworzonej Szansy!").decode('utf8')
            body = (("Nowa szansa o nazwie: %s <br/>Zastała utworzona przez: %s<br/>Dadano do sprzedawcy: %s <br/><a href='%s'>Podgląd szansy</a>").decode('utf8'))\
                    %(lead.name,user.name,lead.user_id.partner_id.name,url)
            
            email_from = user.partner_id.name+"<"+user.partner_id.email+">"
                
            vals = {'email_from': email_from,
                    'email_to': mail_to,
                    'state': 'outgoing',
                    'subject': subject,
                    'body_html': body,
                    'auto_delete': True}
                    
            self.pool.get('mail.mail').create(cr, uid, vals, context=context)
    
    
    