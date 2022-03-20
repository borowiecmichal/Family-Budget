from django import forms

from budgets.models import Budget, ExpanseCategory, Income, Expanse


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'


class ExpanseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpanseCategory
        fields = '__all__'


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'


class ExpanseForm(forms.ModelForm):
    class Meta:
        model = Expanse
        fields = '__all__'
