from django.urls import path
from . import views


urlpatterns = [
    # search and info
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('info', views.info, name='info'),
    # voucher handling
    path('customer/<int:pk>/assignvoucher/', views.add_voucher_link, name='add_voucher_link'),
    path('voucher/', views.VoucherListView.as_view(), name='voucher_list'),
    path('voucher/new', views.create_new_voucher, name='create_new_voucher'),
    path('voucher/<int:pk>',views.VoucherDetailView.as_view(), name='voucher_detail'),
    path('voucher/<int:pk>/update', views.VoucherUpdate.as_view(), name='update_voucher'),
    path('voucher/<int:pk>/delete', views.VoucherDelete.as_view(), name='delete_voucher'),
    # customer handling
    path('customer/', views.CustomerListView.as_view(), name='customer_list'),
    path('customer/<int:pk>', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<int:pk>/update', views.CustomerUpdate.as_view(), name='update_customer'),
    path('customer/<int:pk>/delete', views.CustomerDelete.as_view(), name='delete_customer'),
    # transactions
    path('customer/<int:pk>/addcash/', views.add_cash_cashier, name='add_cash_cashier'),
    path('customer/<int:pk>/deductcash/', views.deduct_cash_cashier, name='deduct_cash_cashier'),
    # logs and reports
    path('log', views.ActivityLog.as_view(), name='activity_log'),
]
