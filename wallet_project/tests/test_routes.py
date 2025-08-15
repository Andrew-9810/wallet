import json

from django.test import TestCase
from rest_framework import status

from wallet.models import Wallet


class TestWallet(TestCase):
    """Тестирование доступности api."""
    PK = 1
    INCORRECT_PK = 6
    AMOUNT = 10
    AMOUNT_EDIT = 5

    @classmethod
    def setUpTestData(cls):
        cls.wallet = Wallet.objects.create(
            pk=cls.PK,
            amount=cls.AMOUNT
        )

    def test_get_balance(self):
        """Проверка доступности баланса кошелька."""
        response = self.client.get(f'/api/v1/wallets/{self.PK}/')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=(f'Запрос /api/v1/wallets/{self.PK}/ должен вернуть'
                 f' status_code=200')
        )

    def test_post_wallet_access(self):
        """Проверка доступности операций DEPOSIT и WITHDRAW."""
        operations = ('DEPOSIT', 'WITHDRAW')
        for operation in operations:
            with self.subTest():
                operation_type = {
                    'operation_type': f'{operation}', 'amount': self.AMOUNT_EDIT
                }
                response = self.client.post(
                    f'/api/v1/wallets/{self.PK}/operation/',
                    data=json.dumps(operation_type),
                    content_type='application/json'
                )
                self.assertEqual(
                    response.status_code, status.HTTP_202_ACCEPTED,
                    msg=(f'/api/v1/wallets/{self.PK}/operation/,'
                         f' операции {operation}, должен вернуть'
                         f' status_code=202')
                )

    def test_post_incorrect_wallet(self):
        """Проверка ввода отсутствующего uuid кошелька."""
        operations = ('DEPOSIT', 'WITHDRAW')
        for operation in operations:
            with self.subTest():
                operation_type = {
                    'operation_type': f'{operation}', 'amount': self.AMOUNT_EDIT
                }
                response = self.client.post(
                    f'/api/v1/wallets/{self.INCORRECT_PK}/operation/',
                    data=json.dumps(operation_type),
                    content_type='application/json'
                )
                self.assertEqual(
                    response.status_code, status.HTTP_404_NOT_FOUND,
                    msg=(f'/api/v1/wallets/{self.INCORRECT_PK}/operation/,'
                         f' операции {operation}, отсутствующего uuid должен '
                         f'вернуть status_code=404')
                )
