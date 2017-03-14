# -*- coding: utf-8 -*-
# Copyright (c) 2017, Arpit Jain and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import frappe.defaults
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname

"""Auto naming for batch creation"""
def autoname_batch(self, method):
		batch_id = self.item +"-"+'.#####'
		self.name =  make_autoname(batch_id)
		self.batch_id = self.name
		

"""batch_creation through Stock Entry and Purchase Recipet"""
def batch_creation(self, method):
	if self.doctype == "Purchase Receipt":
		for chld in self.items:
			chld.batch_no = create_batch(chld.item_code, chld)
	elif not self.update_stock and (self.purpose == 'Material Receipt' or self.purpose=='Manufacture') and self.doctype == "Stock Entry":
		for chld in self.items:
			has_batch=frappe.db.get_value("Item",{"item_code":chld.item_code},["has_batch_no"])
			if(has_batch==1):
				if(chld.production_date and chld.expiry_date):
					chld.batch_no = create_batch(chld.item_code, chld)
				else:
					frappe.throw(_("Please Enter Production And Expiry Dates."))


def create_batch(item_code, chld):
	item = frappe.db.get_value("Item", {'name' : item_code}, 'has_batch_no', as_dict =True)
	if item.get('has_batch_no') == 1:
		batch = frappe.get_doc({
			"doctype": "Batch",
			"item": item_code,
			"production_date": chld.production_date if chld.production_date else "",
			"expiry_date":  chld.expiry_date if chld.expiry_date else "" 
			})
		batch.flags.ignore_permissions = True
		batch.insert()
		return batch.name

def get_remarkfield(self,method):
	if self.voucher_type == "Stock Entry":
		remark = frappe.db.get_value("Stock Entry Detail",{'name':self.voucher_detail_no},["remarks"])
		self.remarks = remark
	