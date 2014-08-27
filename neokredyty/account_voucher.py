# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields, osv
from openerp.addons.mail.mail_message import decode
import pdb

AVAILABLE_METHOD = [
    ('Gotowka', 'Gotówka'),
    ('Przelew', 'Przelew')]

def num2word(n,l="en_US"):
#    wordtable = ["zer","jed","dwa","trz","czt","pie","sze","sie","osi","dzi"]
    sym={
        "en_US": {
            "0": u'zero',
            "x": [u'one',u'two',u'three',u'four',u'five' ,u'six',u'seven',u'eight',u'nine'],
            "1x": [u'ten',u'eleven',u'twelve',u'thirteen',u'fourteen',u'fifteen',u'sixteen',u'seventeen',u'eighteen',u'nineteen'],
            "x0": [u'twenty',u'thirty',u'fourty',u'fifty',u'sixty',u'seventy',u'eighty',u'ninety'],
            "100": u'hundred',
            "1K": u'thousand',
            "1M": u'million',
        },
        "pl_PL": {
            "0": u'zero',
            "x": [u'jeden',u'dwa',u'trzy',u'cztery',u'pięć' ,u'sześć',u'siedem',u'osiem',u'dziewięć'],
            "1x": [u'dziesięć',u'jedenaście',u'dwanaście',u'trzynaście',u'czternaście',u'piętnaście',u'szesnaście',u'siedemnaście',u'osiemnaście',u'dziewiętnaście'],
            "x0":  [u'dwadzieścia',u'trzydzieści',u'czterdzieści',u'pięćdziesiąt',u'sześćdziesiąt',u'siedemdziesiąt',u'osiemdziesiąt',u'dziewięćdziesiąt'],
            "1xx": [u'sto',u'dwieście',u'trzysta',u'czterysta',u'pięćset',u'sześćset',u'siedemset',u'osiemset',u'dziewięćset'],
            "1000" : u'tysiąc',
            "1K": [u'tysięcy',u'tysięcy',u'tysiące',u'tysiące',u'tysiące',u'tysięcy',u'tysięcy',u'tysięcy',u'tysięcy',u'tysięcy', 'tysięcy'],
            "1M" : u'milion',
            "1Ms": [u'milionów',u'milionów',u'miliony',u'miliony',u'miliony',u'milionów',u'milionów',u'milionów',u'milionów',u'milionów'],
       }
    }

    if n==0:
        word = sym[l]["0"]
    elif n<10:
        word = sym[l]["x"][n-1]
    elif n<100:
        if n<20:
            word = sym[l]["1x"][n-10]
        else:
            word = sym[l]["x0"][n/10-2] + (n%10 and " " + num2word(n%10,l) or "")
    elif n<1000:
        if l=="en_US":
            word = sym[l]["x"][n/100-1]+" " + sym[l]["100"]+(n%100 and " "+num2word(n%100,l) or "")
        elif l=="pl_PL":
            word = sym[l]["1xx"][n/100-1] + (n%100 and " "+num2word(n%100,l) or "")
    elif n<1000000:
        if l=="en_US":
            word = num2word(n/1000,l)+" "+sym[l]["1K"]+(n%1000 and " "+num2word(n%1000,l) or "")
        elif l=="pl_PL":
            if n <2000:
                tys = sym[l]["1000"]
            elif n%100000>10000 and n%100000<20000:
                tys = sym[l]["1K"][0]
            else:
                tys = sym[l]["1K"][n/1000%10]
            word = num2word(n/1000,l) +" "+ tys + (n%1000  and " " + num2word(n%1000,l) or "")
    elif n<1000000000:
        if l=="en_US":
            word = num2word(n/1000000,l)+" "+sym[l]["1M"] + (n%1000000  and " " + num2word(n%1000000,l) or "")
        if l=="pl_PL":
            if n <2000000:
                mil = sym[l]["1M"]
            elif n%100000000>10000000 and n%100000000<20000000:
                mil = sym[l]["1Ms"][0]
            else:
                mil = sym[l]["1Ms"][n/1000000%10]
            word = num2word(n/1000000,l) +" "+ mil + (n%1000000  and " " + num2word(n%1000000,l) or "")
    else:
        return  "N/A"
    return word

class account_voucher(osv.Model):
    _inherit = "account.voucher"
     
    def _get_num2word(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        for voucher in self.browse(cr, uid, ids):
            cents = int(round((voucher.amount-int(voucher.amount)),2)*100)
            str_cents = num2word(cents, 'pl_PL')+' groszy'
            string = ''
            
            string = num2word(int(voucher.amount), 'pl_PL')
            res[voucher.id] = string+decode(' złotych ') + str_cents
        return res
     
    _columns = {
        'payment_method': fields.selection(AVAILABLE_METHOD, 'Sposób zapłaty', required=True), 
        'payment_date' : fields.date('Termin zapłaty',),
        'bank_account_id' : fields.many2one('res.partner.bank','Bank',),
        'num_to_word' : fields.function(_get_num2word, type='char', string='Słownie', store=False),
     }












