frappe.ui.form.on("Delivery Note Item", {
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
						refresh_field("items");
						}
					}
				})
		}
	},
 })
cur_frm.cscript.item_code= function(doc, cdt, cdn, from_barcode) {
		var me = this;
		var item = frappe.get_doc(cdt, cdn);

		// clear barcode if setting item (else barcode will take priority)
		if(!from_barcode) {
			item.barcode = null;
		}
		if(item.item_code || item.barcode || item.serial_no) {
			if(!validate_company_and_party()) {
				cur_frm.fields_dict["items"].grid.grid_rows[item.idx - 1].remove();
			} else {
				return this.frm.call({
					method: "erpnext.stock.get_item_details.get_item_details",
					child: item,
					args: {
						args: {
							item_code: item.item_code,
							barcode: item.barcode,
							serial_no: item.serial_no,
							warehouse: item.warehouse,
							customer: me.frm.doc.customer,
							supplier: me.frm.doc.supplier,
							currency: me.frm.doc.currency,
							conversion_rate: me.frm.doc.conversion_rate,
							price_list: me.frm.doc.selling_price_list ||
								 me.frm.doc.buying_price_list,
							price_list_currency: me.frm.doc.price_list_currency,
							plc_conversion_rate: me.frm.doc.plc_conversion_rate,
							company: me.frm.doc.company,
							order_type: me.frm.doc.order_type,
							is_pos: cint(me.frm.doc.is_pos),
							is_subcontracted: me.frm.doc.is_subcontracted,
							transaction_date: me.frm.doc.transaction_date || me.frm.doc.posting_date,
							ignore_pricing_rule: me.frm.doc.ignore_pricing_rule,
							doctype: me.frm.doc.doctype,
							name: me.frm.doc.name,
							project: item.project || me.frm.doc.project,
							qty: item.qty
							
						}
					},

					callback: function(r) {
						if(!r.exc) {
							set_batch_no(doc, cdt, cdn, item, from_barcode)
							me.frm.script_manager.trigger("price_list_rate", cdt, cdn);
						}
					}
				});
			}
		}
	},
	cur_frm.cscript.barcode= function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.barcode=="" || d.barcode==null) {
			// barcode cleared, remove item
			d.item_code = "";
		}
		cur_frm.cscript.item_code(doc, cdt, cdn, true);
	},
	validate_company_and_party= function(doc) {
		var me = this;
		var valid = true;

		$.each(["company", "customer"], function(i, fieldname) {
			if(frappe.meta.has_field(cur_frm.doc.doctype, fieldname && cur_frm.doc.doctype != "Purchase Order")) {
				if (!me.frm.doc[fieldname]) {
					msgprint(__("Please specify") + ": " +
						frappe.meta.get_label(me.frm.doc.doctype, fieldname, me.frm.doc.name) +
						". " + __("It is needed to fetch Item Details."));
						valid = false;
				}
			}
		});
		return valid;
	}

	set_batch_no = function (doc, cdt, cdn, item, from_barcode) {
		if (!from_barcode) {
			// alert("1")
			return frappe.call({
				method:"goodfood_trading.customization.delivery_note.delivery_note.batch_with_closest_expiration",
				args: {"item_code": item.item_code},
				callback: function(r){
					if (r.message){
							if(r.message['batches']){
								item.batch_no =r.message['batches']['batch_id']
								item.expiry_date = r.message['batches']['expiry_date']
								item.production_date =r.message['batches']['production_date']
								refresh_field("items");
							}
					}
				}
			})
		} else {
			// alert("2")
			return frappe.call({
				method:"goodfood_trading.customization.delivery_note.delivery_note.pull_batch_no_accdording_to_barcode",
				args: {"barcode": item.barcode},
				callback: function(r){
					if (r.message){
						item.batch_no =r.message[0]['batch_id']
						item.expiry_date = r.message[0]['expiry_date']
						item.production_date =r.message[0]['production_date']
						refresh_field("items");
					}
				}
			})
		}
	}