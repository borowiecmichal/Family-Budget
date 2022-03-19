import graphene
from django.core.exceptions import PermissionDenied
from graphene import Field
from graphql_jwt.decorators import login_required

from budgets.forms import BudgetForm, ExpanseCategoryForm
from budgets.models import Budget, ExpanseCategory
from budgets.schema import BudgetNode, ExpanseCategoryNode
from utils.mutations import DjangoModelFormRelayMutation, RelayClientIdDeleteMutation


class CreateOrUpdateExpanseCategoryMutation(DjangoModelFormRelayMutation):
    expanseCategory = Field(ExpanseCategoryNode)

    class Meta:
        form_class = ExpanseCategoryForm

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        if form.instance.budget.id not in info.context.user.own_budgets.values_list('budget', flat=True):
            raise PermissionDenied("You don't have access to this object")
        return super(CreateOrUpdateExpanseCategoryMutation, cls).perform_mutate(form, info)


class CreateOrUpdateBudgetMutation(DjangoModelFormRelayMutation):
    budget = Field(BudgetNode)

    class Meta:
        form_class = BudgetForm

    @classmethod
    @login_required
    def get_form_kwargs(cls, root, info, **input):
        kwargs = super(CreateOrUpdateBudgetMutation, cls).get_form_kwargs(root, info, **input)
        kwargs['data']['participants'].append(info.context.user.id)
        return kwargs

    @classmethod
    def perform_mutate(cls, form, info):
        if form.instance.id is not None \
                and form.instance.id not in info.context.user.own_budgets.values_list('budget', flat=True):
            raise PermissionDenied("You don't have access to this object")
        set_owner = form.instance.id is None
        form.save()
        if set_owner:
            owner_association = form.instance.participant_associations.get(participant=info.context.user)
            owner_association.is_owner = True
            owner_association.save()
        return cls(errors=[], budget=form.instance)


class DeleteBudgetMutation(RelayClientIdDeleteMutation):
    class Meta:
        model_class = Budget

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        return queryset.filter(participant_associations__is_owner=True, participant_associations__participant=info.context.user,)


class DeleteExpanseCategory(RelayClientIdDeleteMutation):
    class Meta:
        model_class = ExpanseCategory

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        return queryset.filter(
            budget__participant_associations__is_owner=True,
            budget__participant_associations__participant=info.context.user,
        )


class Mutations(graphene.ObjectType):
    create_or_update_budget = CreateOrUpdateBudgetMutation.Field()
    create_or_update_expanse_category = CreateOrUpdateExpanseCategoryMutation.Field()
    delete_budget = DeleteBudgetMutation.Field()
    delete_expanse_category = DeleteExpanseCategory.Field()
