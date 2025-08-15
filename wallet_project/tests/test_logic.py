import json

from django.test import TestCase
from rest_framework import status

from wallet.models import Wallet


class TestWallet(TestCase):
    """Тестирование api."""
    PK = 1
    AMOUNT = 10
    AMOUNT_EDIT = 5

    def setUp(self):
        self.wallet = Wallet.objects.create(
            pk=self.PK,
            amount=self.AMOUNT
        )

    def tearDown(self):
        self.wallet = Wallet.objects.filter(pk=self.PK).delete()

    def test_get_balance_amount(self):
        """Проверка баланса кошелька."""
        response = self.client.get(f'/api/v1/wallets/{self.PK}/')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data, {"amount": self.AMOUNT},
            msg=(f'Запрос /api/v1/wallets/{self.PK}/ должен вернуть'
                 f' баланс кошелька равный {self.AMOUNT}')
        )

    def test_post_wallet_deposit(self):
        """Проверка работы операции DEPOSIT."""
        operation = 'DEPOSIT'
        operation_type = {
            'operation_type': f'{operation}', 'amount': self.AMOUNT_EDIT
        }
        response = self.client.post(
            f'/api/v1/wallets/{self.PK}/operation/',
            data=json.dumps(operation_type),
            content_type='application/json'
        )
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data, {"amount": self.AMOUNT + self.AMOUNT_EDIT},
            msg=(f'/api/v1/wallets/{self.PK}/operation/, неверно посчитана'
                 f' операция {operation}')
        )

    def test_post_wallet_withdraw(self):
        """Проверка работы операции WITHDRAW."""
        operation = 'WITHDRAW'
        operation_type = {
            'operation_type': f'{operation}', 'amount': self.AMOUNT_EDIT
        }
        response = self.client.post(
            f'/api/v1/wallets/{self.PK}/operation/',
            data=json.dumps(operation_type),
            content_type='application/json'
        )
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data, {"amount": self.AMOUNT - self.AMOUNT_EDIT},
            msg=(f'/api/v1/wallets/{self.PK}/operation/, неверно посчитана'
                 f' операция {operation}')
        )

    def test_post_incorrect_operation(self):
        """Проверка ввода некорректной операции."""
        operation = 'OPERATION'
        operation_type = {
            'operation_type': f'{operation}', 'amount': self.AMOUNT_EDIT
        }
        response = self.client.post(
            f'/api/v1/wallets/{self.PK}/operation/',
            data=json.dumps(operation_type),
            content_type='application/json'
        )
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data, {'operation_type': 'operation error'},
            msg=(f'/api/v1/wallets/{self.PK}/operation/, некорректный'
                 ' operation_type должен возвращать'
                 ' {"operation_type": "operation error"}')
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg=(f'/api/v1/wallets/{self.PK}/operation/, некорректный'
                 f' operation_type должен возвращать статус 400')
        )

    def test_post_field_lack(self):
        """Проверка ввода некорректных данных в поле amount."""
        values = (
            ('1', 'str'),
            (0, 'int')
        )
        for value, check in values:
            with self.subTest():
                operation = 'WITHDRAW'
                operation_type = {
                    'operation_type': f'{operation}', 'amount': value
                }
                response = self.client.post(
                    f'/api/v1/wallets/{self.PK}/operation/',
                    data=json.dumps(operation_type),
                    content_type='application/json'
                )
                data = json.loads(response.content.decode('utf-8'))
                self.assertEqual(
                    data, {'amount': [f"type:<class '{check}'>", value]},
                    msg=(f'/api/v1/wallets/{self.PK}/operation/, при вводе'
                         ' некорректных данных в поле amount должен возвращать'
                         'класс и значение неверно введенной переменной')
                )
                self.assertEqual(
                    response.status_code, status.HTTP_400_BAD_REQUEST,
                    msg=(f'/api/v1/wallets/{self.PK}/operation/, при вводе'
                         ' некорректных данных в поле amount'
                         ' должен возвращаться статус 400')
                )
