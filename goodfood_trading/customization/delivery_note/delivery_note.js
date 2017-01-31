frappe.ui.form.on("Delivery Note Item", {
	item_code: function (doc, cdt, cdn) {
		// var item = frappe.get_doc(cdt, cdn);
		var item = locals[cdt][cdn]
		return frappe.call({
			method:"goodfood_trading.customization.delivery_note.delivery_note.batch_with_closest_expiration",
			args: {"item_code": item.item_code},
			callback: function(r){
				if (r.message){
					console.log(item)
					console.log(item.batch_no)
					item.batch_no ="Mac Book-00013"
					// dfrappe.model.set_value(cdt, cdn, "batch_no","Mac Book-00013");
					frappe.model.set_value(cdt, cdn, "expiry_date",r.message[0]['expiry_date']);
					frappe.model.set_value(cdt, cdn, "production_date",r.message[0]['production_date']);
					// cur_frm.cscript.batch_no(cdt, cdn)
					cur_frm.refresh_fields();
					// console.log("0000000000000000000000")
					console.log(JSON.stringify(r.message))
					 
				}
			}
		})
	},
	batch_no: function(doc, cdt, cdn) {
		var item = frappe.get_doc(cdt, cdn);
		if (item.item_code && item.batch_no) {
			return frappe.call({
			method:"goodfood_trading.customization.delivery_note.delivery_note.batch_according_to_batch_no",
			args: {"item_code": item.item_code,
					"batch_no": item.batch_no},
			callback: function(r){
				if (r.message){
					console.log(JSON.stringify(r.message))
					frappe.model.set_value(cdt, cdn, "expiry_date",r.message[0]['expiry_date']);
					frappe.model.set_value(cdt, cdn, "production_date",r.message[0]['production_date']);
					// cur_frm.cscript.batch_no(cdt, cdn)
					cur_frm.refresh_fields();
					// console.log("0000000000000000000000")
					}
				}
			})
		}
	}
 
})
// cur_frm.cscript.batch_no = function(cdt, cdn) {
// 	var item = frappe.get_doc(cdt, cdn);
// 	item.batch_no = "Mac Book-00013"
// 	cur_frm.refresh_fields();
// }