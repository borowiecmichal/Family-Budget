from django import forms

from budgets.models import Budget


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'

    def __init__(self, **kwargs):
        super(BudgetForm, self).__init__(**kwargs)
