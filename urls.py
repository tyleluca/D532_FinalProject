from django.urls import path
from coffee import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('purchase/', views.purchase_coffee, name='purchase_coffee'),
    path('add_product/', views.add_product, name='add_product'),
    path('sales_dashboard/', views.sales_dashboard, name='sales_dashboard')
]
