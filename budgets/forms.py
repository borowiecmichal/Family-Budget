from django import forms

from budgets.models import Budget, ExpanseCategory


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'


class ExpanseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpanseCategory
        fields = '__all__'

