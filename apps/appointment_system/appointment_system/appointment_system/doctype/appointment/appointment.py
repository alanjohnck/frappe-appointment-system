import frappe
from frappe.model.document import Document

class Appointment(Document):
    def validate(self):
        # Check if another confirmed appointment exists for same staff and time
        conflict = frappe.db.exists(
            "Appointment",
            {
                "staff": self.staff,
                "appointment_time": self.appointment_time,
                "status": "Confirmed",
                "name": ["!=", self.name],
            },
        )

        if conflict:
            frappe.throw(f"Staff {self.staff} already has an appointment at {self.appointment_time}.")

 def has_permission(self, ptype=None, user=None):
        user = user or frappe.session.user
        if user in ("Administrator", "Guest"):
            return True
        if frappe.has_role(user, "System Manager"):
            return True
        biz = frappe.db.get_value("Business", {"owner_user": user})
        if biz and self.business == biz:
            return True
        return False

