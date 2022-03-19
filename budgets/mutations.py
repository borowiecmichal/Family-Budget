import graphene
from graphql_jwt.decorators import login_required

from budgets.forms import BudgetForm
from utils.mutations import DjangoFormRelayMutation


class CreateBudgetMutation(DjangoFormRelayMutation):
    class Meta:
        form_class = BudgetForm

    @classmethod
    @login_required
    def get_form_kwargs(cls, root, info, **input):
        kwargs = super(CreateBudgetMutation, cls).get_form_kwargs(root, info, **input)
        kwargs['data']['participants'].append(info.context.user.id)
        return kwargs

    @classmethod
    def perform_mutate(cls, form, info):
        form.save()
        owner_association = form.instance.participant_associations.get(participant=info.context.user)
        owner_association.is_owner = True
        owner_association.save()
        return cls(errors=[], **form.cleaned_data)


class Mutations(graphene.ObjectType):
    create_budget = CreateBudgetMutation.Field()
