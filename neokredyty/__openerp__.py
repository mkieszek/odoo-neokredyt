# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Neo Kredyty',
    'version': '0.1',
    'category': 'Neo Kredyty',
    'description': """ """,
    'author': 'Via IT Solution',
    'website': 'http://www.viait.pl ',
    'depends': ['crm','product','document','account_invoice_pl_og','print_receipt'],
    'data': ['data/crm_lead_data.xml',
             'data/neo_product_data.xml',
             'data/neo_credit_stage_data.xml',
             'security/neo_security.xml',
             'security/ir.model.access.csv'],
    'demo': [],
    'test':[],
    'installable': True,
    'images': [],
    'update_xml' : ['view/res_partner_view.xml',
                    'view/crm_lead_view.xml',
                    'view/neo_credit_view.xml',
                    'view/neo_product_view.xml',
                    'view/voucher_sales_purchase_view.xml',
                    'view/account_voucher_view.xml'],
    'sequence': 1001,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
# -*- coding: utf-8 -*-