from django.db import models
from django_extensions.db.models import TimeStampedModel

from budgets.constants import DEFAULT_EXPANSE_CATEGORIES_NAMES


class ExpanseCategory(models.Model):
    name = models.CharField(max_length=254)
    budget = models.ForeignKey('budgets.Budget', related_name='expanse_categories', on_delete=models.CASCADE)


class Income(TimeStampedModel):
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.CharField(max_length=254)
    transaction_date = models.DateField()
    budget = models.ForeignKey('budgets.Budget', related_name='incomes', on_delete=models.CASCADE)


class Expanse(TimeStampedModel):
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.CharField(max_length=254)
    transaction_date = models.DateField()
    budget = models.ForeignKey('budgets.Budget', related_name='expanses', on_delete=models.CASCADE)
    category = models.ForeignKey(ExpanseCategory, related_name='expanses', null=True, on_delete=models.SET_NULL)


class Budget(TimeStampedModel):
    name = models.CharField(max_length=254)
    participants = models.ManyToManyField('users.BaseUser', through='BudgetParticipant')

    def save(self, **kwargs):
        super(Budget, self).save(**kwargs)
        for category in DEFAULT_EXPANSE_CATEGORIES_NAMES:
            ExpanseCategory.objects.create(name=category, budget=self)


class BudgetParticipant(TimeStampedModel):
    participant = models.ForeignKey('users.BaseUser', related_name='budgets', on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, related_name='participant_associations', on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)
    can_add_components = models.BooleanField(default=False)
