import graphene
from django.core.exceptions import ValidationError
from graphene import Field
from graphql_jwt.decorators import login_required

from budgets.forms import BudgetForm
from budgets.schema import BudgetNode
from utils.mutations import DjangoModelFormRelayMutation


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
        if form.instance.id is not None and form.instance.id not in info.context.user.own_budgets.values_list('budget', flat=True):
            raise ValidationError("You don't have access to this object")
        set_owner = form.instance.id is None
        form.save()
        if set_owner:
            owner_association = form.instance.participant_associations.get(participant=info.context.user)
            owner_association.is_owner = True
            owner_association.save()
        return cls(errors=[], budget=form.instance)


class Mutations(graphene.ObjectType):
    create_or_update_budget = CreateOrUpdateBudgetMutation.Field()
