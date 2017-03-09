frappe.ui.form.on("Stock Entry Detail", {
	batch_no: function(doc, cdt, cdn) {
		var item = frappe.get_doc(cdt, cdn);
		if (item.item_code && item.batch_no) {
			return frappe.call({
				method:"goodfood_trading.customization.delivery_note.delivery_note.batch_according_to_batch_no",
				args: {"item_code": item.item_code,
						"batch_no": item.batch_no},
				callback: function(r){
					if (r.message){
						item.expiry_date = r.message[0]['expiry_date']
						item.production_date =r.message[0]['production_date']
						item.qty = 0.0
						item.final_batch_qty = 0.0
						refresh_field("items");
						cur_frm.cscript.batch_no(doc, cdt, cdn, true)
						}
				}
			})
		}
	},
	/*Reconciliation mechanism for Batch Controlled Items*/
	final_batch_qty: function(doc, cdt, cdn) {
		var item = frappe.get_doc(cdt, cdn);
		if (item.actual_batch_qty && item.final_batch_qty < item.actual_batch_qty ) {
			item.qty = -(item.actual_batch_qty - item.final_batch_qty);
			refresh_field("items");
		}else {
			frappe.msgprint(__("Batch Qty After Reconciliation <b>{0}</b> should not be greater or equal than Actual Batch Qty <b>{1}</b>", [item.final_batch_qty , item.actual_batch_qty]));
		}
	},

// Added BY Khushal
	expiry_date:function(doc,cdt,cdn){
		var d = locals[cdt][cdn]
		var prod_date=new Date(d.production_date)
		var exp_date=new Date(d.expiry_date)
		if(prod_date>exp_date){
		msgprint(__("Production date must not greater than Expiry Date"))
		 	d.production_date=""
		 	d.expiry_date=""
		 	refresh_field("items")
		}
	}
})

frappe.ui.form.on("Stock Entry", {
	update_stock: function(doc, cdt, cdn) {
		if (cint(cur_frm.doc.update_stock)==1) {
			  // hide_field(fild);
			var df = frappe.meta.get_docfield("Stock Entry Detail","qty", cdn);
			df.read_only = 1;
		}
		else {
			//hide_field(child_fields);
			var df = frappe.meta.get_docfield("Stock Entry Detail","qty", cdn);
			df.read_only = 0;
		}
	}
})

cur_frm.cscript.item_code= function(doc, cdt, cdn) {
		/* Display batch_qty_reconciliation fields to reconcile batch qty */
		chld_fld=['conversion_factor']
		batch_qty_reconciliation = ['actual_batch_qty','final_batch_qty']
		cur_frm.fields_dict['items'].grid.set_column_disp(batch_qty_reconciliation,
		(cint(cur_frm.doc.update_stock)==1 ? true : false));

		/* Mandatory  batch_qty_reconciliation fields to reconcile batch qty */
		cur_frm.fields_dict['items'].grid.toggle_reqd("actual_batch_qty", (cint(cur_frm.doc.update_stock)==1 ? true : false));
		cur_frm.fields_dict['items'].grid.toggle_reqd("final_batch_qty", (cint(cur_frm.doc.update_stock)==1 ? true : false));
		
		var d = locals[cdt][cdn];
		// console.log(JSON.stringify(d))
		if(d.item_code) {
			args = {
				'item_code'			: d.item_code,
				'warehouse'			: cstr(d.s_warehouse) || cstr(d.t_warehouse),
				'transfer_qty'		: d.transfer_qty,
				'serial_no	'		: d.serial_no,
				'bom_no'			: d.bom_no,
				'expense_account'	: d.expense_account,
				'cost_center'		: d.cost_center,
				'company'			: cur_frm.doc.company,
				'qty'				: d.qty,
				'posting_date'		: cur_frm.doc.posting_date,
				'posting_time'		: cur_frm.doc.posting_time,
				'purpose'			: cur_frm.doc.purpose,
				'update_stock'		: cur_frm.doc.update_stock
				
			};
			return frappe.call({
				method: "goodfood_trading.customization.stock_entry.stock_entry.get_item_details",
				args: {args : args },
				callback: function(r) {
					if(r.message) {
						var d = locals[cdt][cdn];
						$.each(r.message, function(k, v) {
							d[k] = v;
							 // console.log("#####",[k,v])
						});
						// d.batch_no = "chair-00010"
						refresh_field("items");
						cur_frm.cscript.batch_no(doc, cdt, cdn, true)
						// refresh_field("items");
					}
				}
			});
		}
	},

cur_frm.cscript.batch_no= function(doc, cdt, cdn, item_code) {
	var item = frappe.get_doc(cdt, cdn);
		if(item.t_warehouse && item.item_code && item.batch_no) {
		    return this.frm.call({
		        method: "erpnext.stock.get_item_details.get_batch_qty",
		        child: item,
		        args: {
		           "batch_no": item.batch_no,
		           "warehouse": item.t_warehouse,
		           "item_code": item.item_code
		        },
		         "fieldname": "actual_batch_qty"
		    });
		}

}
