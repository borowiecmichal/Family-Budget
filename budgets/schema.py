import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from budgets.models import Budget


class BudgetNode(DjangoObjectType):
    class Meta:
        model = Budget
        filter_fields = ['name', 'participants']
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    budget = relay.Node.Field(BudgetNode)
    budgets = DjangoFilterConnectionField(BudgetNode)

