# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "goodfood_trading"
app_title = "GoodFood Trading"
app_publisher = "Arpit Jain"
app_description = "good food trading"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "arpit.j@indictranstech.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/goodfood_trading/css/goodfood_trading.css"
# app_include_js = "/assets/goodfood_trading/js/goodfood_trading.js"
# app_include_js = "assets/js/good_friend_trading.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/goodfood_trading/css/goodfood_trading.css"
# web_include_js = "/assets/goodfood_trading/js/goodfood_trading.js"

# include js in page
# page_js = {"pos" : "public/page/poss.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "goodfood_trading.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "goodfood_trading.install.before_install"
# after_install = "goodfood_trading.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "goodfood_trading.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doctype_js = {
   "Delivery Note":["customization/delivery_note/delivery_note.js"],
   "Sales Invoice":["customization/sales_invoice/sales_invoice.js"]
}

doc_events = {
	"Batch": {
		"before_insert": "goodfood_trading.customization.customization.autoname_batch"
	},
	"Stock Entry" :{
		"before_insert": "goodfood_trading.customization.customization.batch_creation"
	},
	"Purchase Receipt" :{
		"before_insert": "goodfood_trading.customization.customization.batch_creation"
	}
}

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"goodfood_trading.tasks.all"
# 	],
# 	"daily": [
# 		"goodfood_trading.tasks.daily"
# 	],
# 	"hourly": [
# 		"goodfood_trading.tasks.hourly"
# 	],
# 	"weekly": [
# 		"goodfood_trading.tasks.weekly"
# 	]
# 	"monthly": [
# 		"goodfood_trading.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "goodfood_trading.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "goodfood_trading.event.get_events"
# }

fixtures= ['Custom Script','Property Setter','Custom Field']