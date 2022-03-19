import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from budgets.models import Budget


class BudgetNode(DjangoObjectType):
    class Meta:
        model = Budget
        filter_fields = ['name', 'participants']
        interfaces = (relay.Node, )

    @classmethod
    @login_required
    def get_node(cls, info, id):
        super(BudgetNode, cls).get_node(info, id)


class Query(graphene.ObjectType):
    budget = relay.Node.Field(BudgetNode)
    budgets = DjangoFilterConnectionField(BudgetNode)

    @login_required
    def resolve_budgets(self, info, **kwargs):
        return Budget.objects.filter(participants=info.context.user)

