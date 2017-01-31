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
	for chld in self.items:
		chld.batch_no = create_batch(chld.item_code, chld)
		
def create_batch(item_code, chld):
	batch = frappe.get_doc({
		"doctype": "Batch",
		"item": item_code,
		"production_date": chld.production_date if chld.production_date else "",
		"expiry_date":  chld.expiry_date if chld.expiry_date else "" 
		})
	batch.flags.ignore_permissions = True
	batch.insert()
	return batch.name