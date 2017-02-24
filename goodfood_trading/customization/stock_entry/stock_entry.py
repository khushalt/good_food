# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.defaults
from frappe import _
from frappe.utils import cstr, cint, flt, comma_or, getdate, nowdate, formatdate, format_time
from erpnext.stock.utils import get_incoming_rate
from erpnext.stock.stock_ledger import get_previous_sle, NegativeStockError
from erpnext.stock.get_item_details import get_bin_details, get_default_cost_center, get_conversion_factor
from erpnext.manufacturing.doctype.bom.bom import validate_bom_no
import json


@frappe.whitelist()
def get_item_details(args=None, for_update=False):
		arg = json.loads(args)
		item = frappe.db.sql("""select stock_uom, description, image, item_name,
			expense_account, buying_cost_center, item_group from `tabItem`
			where name = %s
				and disabled=0
				and (end_of_life is null or end_of_life='0000-00-00' or end_of_life > %s)""",
			(arg.get('item_code'), nowdate()), as_dict = 1)

		query =frappe.db.sql("""SELECT `item`,`name`,`batch_id` as batch_no,  date(production_date) as production_date,
			date(expiry_date) as expiry_date  from `tabBatch` where item='{0}' and DATEDIFF(expiry_date, date(now())) >= 2""".format(arg.get('item_code')),as_dict=1)
		# print arg.get('update_stock'), "mmmmmmmmmmmmmmmmm"
		if item and arg.get('purpose') == 'Material Receipt' and arg.get('update_stock') == True:
			batches ={}
			d ={}      
			for i in query:                    
			    d[i['item']] = min([row['expiry_date'] for row in query if row['item'] == i['item']])
			for i in query:
				if i['expiry_date'] in d.values():
					batches['batches'] =i
			item[0].update(batches.get('batches'))
		
		if not item:
			frappe.throw(_("Item {0} is not active or end of life has been reached").format(arg.get("item_code")))

		item = item[0]

		ret = {
			'uom'			      	: item.stock_uom,
			'stock_uom'			  	: item.stock_uom,
			'description'		  	: item.description,
			'image'					: item.image,
			'item_name' 		  	: item.item_name,
			'expense_account'		: arg.get("expense_account"),
			'cost_center'			: get_default_cost_center(arg, item),
			'qty'					: 0,
			'transfer_qty'			: 0,
			'conversion_factor'		: 1,
			'batch_no'				: item.batch_no if arg.get('update_stock') == True else '',
			'actual_qty'			: 0,
			'basic_rate'			: 0,
			'serial_no'				: '',
			'production_date'		: item.production_date if arg.get('update_stock') == True else '',
			'expiry_date'			: item.expiry_date if arg.get('update_stock') == True else ''
		}
		for d in [["Account", "expense_account", "default_expense_account"],
			["Cost Center", "cost_center", "cost_center"]]:
				company = frappe.db.get_value(d[0], ret.get(d[1]), "company")
				if not ret[d[1]] or (company and arg.get('company') != company):
					ret[d[1]] = frappe.db.get_value("Company", arg.get('company'), d[2]) if d[2] else None

		# update uom
		if arg.get("uom") and for_update:
			ret.update(get_uom_details(arg))

		if not ret["expense_account"]:
			ret["expense_account"] = frappe.db.get_value("Company", arg.get('company'), "stock_adjustment_account")

		arg['posting_date'] = arg.get('posting_date')
		arg['posting_time'] = arg.get('posting_time')

		stock_and_rate = arg.get('warehouse') and get_warehouse_details(arg) or {}
		ret.update(stock_and_rate)
		# print ret, "------------"
		return ret

def get_uom_details(args):
		"""Returns dict `{"conversion_factor": [value], "transfer_qty": qty * [value]}`

		:param args: dict with `item_code`, `uom` and `qty`"""
		conversion_factor = get_conversion_factor(args.get("item_code"), args.get("uom")).get("conversion_factor")

		if not conversion_factor:
			frappe.msgprint(_("UOM coversion factor required for UOM: {0} in Item: {1}")
				.format(args.get("uom"), args.get("item_code")))
			ret = {'uom' : ''}
		else:
			ret = {
				'conversion_factor'		: flt(conversion_factor),
				'transfer_qty'			: flt(args.get("qty")) * flt(conversion_factor)
			}
		return ret

def get_warehouse_details(args):
	if isinstance(args, basestring):
		args = json.loads(args)

	args = frappe._dict(args)

	ret = {}
	if args.warehouse and args.item_code:
		args.update({
			"posting_date": args.posting_date,
			"posting_time": args.posting_time,
		})
		ret = {
			"actual_qty" : get_previous_sle(args).get("qty_after_transaction") or 0,
			"basic_rate" : get_incoming_rate(args)
		}

	return ret