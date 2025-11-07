import frappe

@frappe.whitelist()
def get_business_dashboard_data():
    user = frappe.session.user
    business = frappe.db.get_value("Business", {"owner_user": user})

    if not business:
        return {"appointments": [], "staff": []}

    appointments = frappe.get_all(
        "Appointment",
        filters={"business": business, "status": "Pending"},
        fields=["name", "customer", "service", "appointment_time"]
    )

    staff = frappe.get_all(
        "Staff",
        filters={"business": business},
        fields=["name"]
    )

    return {"appointments": appointments, "staff": staff}


@frappe.whitelist()
def update_appointment_status(name, status):
    """Approve or reject an appointment"""
    doc = frappe.get_doc("Appointment", name)
    user = frappe.session.user
    business = frappe.db.get_value("Business", {"owner_user": user})

    if doc.business != business:
        frappe.throw("You are not allowed to modify this appointment")

    doc.status = status
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return "success"

