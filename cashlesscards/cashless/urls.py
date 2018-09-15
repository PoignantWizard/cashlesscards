from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('info', views.info, name='info'),
    path('customer/<int:pk>', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<int:pk>/addcash/', views.add_cash_cashier, name='add_cash_cashier'),
    path('customer/<int:pk>/deductcash/', views.deduct_cash_cashier, name='deduct_cash_cashier'),
    path('log', views.ActivityLog.as_view(), name='activity_log'),
    path('customer/<int:pk>/assignvoucher/', views.add_voucher_link, name='add_voucher_link'),
]
