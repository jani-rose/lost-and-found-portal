from django.urls import path
from . import views

urlpatterns = [

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
    path(
        'report-item/',
        views.report_item,
        name='report_item'
    ),
    path(
        'update-status/<int:item_id>/',
        views.update_status,
        name='update_status'
    ),
    path(
        'all-reports/',
        views.all_reports,
        name='all_reports'
    ),
    path(
        'item/<int:item_id>/',
        views.item_detail,
        name='item_detail'
    ),
    path(
        'item/<int:item_id>/confirm/',
        views.confirm_recovery,
        name='confirm_recovery'
    ),
    path(
        'item/<int:item_id>/message/',
        views.send_message,
        name='send_message'
    ),
    path(
        'inbox/',
        views.inbox_view,
        name='inbox'
    ),
    path(
        'inbox/<int:item_id>/<int:other_user_id>/',
        views.inbox_view,
        name='inbox_thread'
    ),
]