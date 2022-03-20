import django_filters

from budgets.models import Income, Expanse


class IncomeFilterSet(django_filters.FilterSet):
    amount_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    amount_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    transaction_date_gt = django_filters.NumberFilter(field_name='transaction_date', lookup_expr='gt')
    transaction_date_lt = django_filters.NumberFilter(field_name='transaction_date', lookup_expr='lt')

    class Meta:
        model = Income
        fields = 'amount', 'transaction_date', 'budget'


class ExpanseFilterSet(IncomeFilterSet):
    class Meta:
        model = Expanse
        fields = 'amount', 'transaction_date', 'budget'
