# -*- coding: utf-8 -*-
# Copyright (c) 2016, Arpit Jain and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.document import Document
import frappe.defaults
import datetime
from datetime import timedelta


@frappe.whitelist()
def batch_with_closest_expiration(item_code):
	query =frappe.db.sql("""SELECT `item`,`name`,`batch_id` as batch_id,  date(production_date) as production_date,
	 date(expiry_date) expiry_date  from `tabBatch` where item='{0}' and DATEDIFF(expiry_date, date(now())) >= 2""".format(item_code),as_dict=1)
	batches ={}
	d ={}      
	for i in query:                    
	    d[i['item']] = min([row['expiry_date'] for row in query if row['item'] == i['item']])
	for i in query:
	    if i['expiry_date'] in d.values():
	    	batches['batches'] =i
	return batches

@frappe.whitelist()
def batch_according_to_batch_no(item_code, batch_no):
	query = """SELECT expiry_date, `production_date` as production_date, 
		min(DATEDIFF(expiry_date, date(now()))) as diff 
		from `tabBatch` 
		where item='{0}' 
			and DATEDIFF(expiry_date, date(now())) >= 2 and batch_id ='{1}'""".format(item_code, batch_no)
	result = frappe.db.sql(query,as_dict=1)
	return result


@frappe.whitelist()
def pull_batch_no_accdording_to_barcode(barcode):
	query = """SELECT `name`,`batch_id`, expiry_date, `production_date` as production_date, `item`, 
		min(DATEDIFF(expiry_date, date(now()))) as diff 
		from `tabBatch` 
		where item in (select name from `tabItem` where barcode ='{0}') 
			and DATEDIFF(expiry_date, date(now())) >= 2""".format(barcode)
	result = frappe.db.sql(query,as_dict=1)
	return result

