from api.admin.base import BaseAdminView


class AdminView(BaseAdminView):
    required_role = 'superadmin'
    column_display_all_relations = True
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = ['roles.name', 'email', 'first_name', 'last_name', 'active']
    column_exclude_list = ['password']
    column_details_exclude_list = ['password']
    column_filters = ['email', 'first_name', 'last_name', 'active']
    can_export = True
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    edit_modal = True
    create_modal = True
    details_modal = True


class SubscriberView(BaseAdminView):
    column_display_all_relations = False
    form_excluded_columns = ['date_created', 'date_updated', 'transactions']
    can_edit = False
    can_create = False
    can_delete = False
    details_modal = True
    can_view_details = True
    can_export = True


class CategoryView(BaseAdminView):
    column_display_all_relations = False
    form_excluded_columns = ['transactions', 'subscribers', 'billing_logs']
    column_labels = {'price': "Price (in kobo)", 'validity': "Validity (in days)"}
    can_edit = True
    can_create = True
    can_delete = False
    details_modal = True
    can_view_details = True
    can_export = True


class BillingView(BaseAdminView):
    column_display_all_relations = False
    can_edit = False
    can_create = False
    can_delete = False
    column_list = ['user', 'category', 'price', 'items', 'mode', 'txn_type', 'date_created']


class UnsubscriptionView(BaseAdminView):
    column_display_all_relations = False
    can_edit = False
    can_create = False
    column_list = ['user', 'category', 'mode', 'date_created']
