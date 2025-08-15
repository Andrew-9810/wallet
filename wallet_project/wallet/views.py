from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from wallet.models import Wallet
from wallet.serializers import WalletSerializer


@api_view(['POST'])
def operation(request, wallet_uuid):
    """Выполнение операций над кошельком."""
    wallet = get_object_or_404(Wallet, pk=wallet_uuid)
    operation_type = request.data.get('operation_type')
    amount = request.data.get('amount')
    if operation_type in ['DEPOSIT', 'WITHDRAW']:
        if isinstance(amount, int) and amount > 0:
            if operation_type == 'DEPOSIT':
                result = wallet.amount + amount
            else:
                result = wallet.amount - amount
            serializer = WalletSerializer(wallet, data={'amount': result})
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_202_ACCEPTED
                )
        return Response(
            {'amount': [f'type:{type(amount)}', amount]},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        return Response(
            {'operation_type': 'operation error'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def balance(request, wallet_uuid):
    """Получение баланса."""
    wallet = get_object_or_404(Wallet, pk=wallet_uuid)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data, status=status.HTTP_200_OK)
