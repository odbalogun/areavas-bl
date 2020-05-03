from api.admin.base import BaseAdminView


class UserView(BaseAdminView):
    column_editable_list = ['first_name', 'last_name', 'age']
    column_searchable_list = ['first_name', 'last_name', 'age']
    column_exclude_list = None
    column_details_exclude_list = None
    column_filters = ['first_name', 'last_name', 'age', 'created_at', 'updated_at']
    can_export = True
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    edit_modal = True
    create_modal = True
    details_modal = True


class AdminView(BaseAdminView):
    required_role = 'superadmin'
    column_display_all_relations = True
    column_editable_list = ['email', 'first_name', 'last_name', 'active']
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