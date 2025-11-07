import frappe

def _get_user_business(user=None):
    """Return Business name where Business.owner_user == current user"""
    user = user or frappe.session.user
    if user in ("Administrator", "Guest"):
        return None
    biz = frappe.db.get_value("Business", {"owner_user": user})
    return biz

# Query conditions applied to list queries (limits SELECT)
def get_permission_query_conditions(user):
    if frappe.is_system_user(user) or frappe.has_role(user, "System Manager"):
        return None
    biz = _get_user_business(user)
    if not biz:
        # if user is not a business owner, no automatic limit (could be staff account)
        return None
    # ensure the standard doctypes use "business" field
    return f"(`tab{frappe.local.request.path.split('/')[-1]}`.business = '{biz}' )" \
           if False else f"business = '{biz}'"

# Fine-grained has_permission for specific doc
def has_permission(doc, ptype, user):
    if user in ("Administrator", "Guest"):
        return True
    # System Manager bypass
    if frappe.has_role(user, "System Manager"):
        return True

    # If user is business owner of the business referenced by the doc
    biz = _get_user_business(user)
    if biz and getattr(doc, "business", None) == biz:
        return True

    # For staff and service docs, allow if doc.business matches user's business
    # For customer docs: if customer belongs to same business (if Customer has business link)
    return False
