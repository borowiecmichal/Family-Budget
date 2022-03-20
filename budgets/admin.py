from django.contrib import admin

from budgets.models import Budget, Income, Expanse, BudgetParticipant

admin.site.register(Budget)
admin.site.register(Income)
admin.site.register(Expanse)
admin.site.register(BudgetParticipant)
