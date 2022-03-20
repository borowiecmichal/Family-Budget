from django.contrib import admin

from budgets.models import Budget, Income, Expanse, BudgetParticipant, ExpanseCategory

admin.site.register(Budget)
admin.site.register(Income)
admin.site.register(Expanse)
admin.site.register(BudgetParticipant)
admin.site.register(ExpanseCategory)
