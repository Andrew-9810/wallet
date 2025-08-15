from django.db import models


class Wallet(models.Model):
    """Модель Wallet."""
    amount = models.IntegerField(default=0, blank=True, verbose_name="amount")

    def __str__(self):
        return f'{self.pk}: {self.amount}'