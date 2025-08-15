from django.contrib import admin
from django.urls import path

from wallet import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # Получение баланса кошелька.
    path('api/v1/wallets/<int:wallet_uuid>/', views.balance, name='balance'),
    # Выполнение операций над кошельком.
    path('api/v1/wallets/<int:wallet_uuid>/operation/', views.operation,
         name='operation'
    ),
]
