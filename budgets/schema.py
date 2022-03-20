import graphene
from django.core.exceptions import PermissionDenied
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from budgets.models import Budget, ExpanseCategory, Income, Expanse


class ExpanseCategoryNode(DjangoObjectType):
    class Meta:
        model = ExpanseCategory
        filter_fields = ['name', 'budget']
        interfaces = (relay.Node, )

    @classmethod
    @login_required
    def get_node(cls, info, id):
        category = super(ExpanseCategoryNode, cls).get_node(info, id)
        if info.context.user not in category.budget.participants.all():
            raise PermissionDenied("You don't have access to this object")
        return category


class BudgetNode(DjangoObjectType):
    class Meta:
        model = Budget
        filter_fields = ['name', 'participants']
        interfaces = (relay.Node, )

    @classmethod
    @login_required
    def get_node(cls, info, id):
        budget = super(BudgetNode, cls).get_node(info, id)
        if info.context.user not in budget.participants.all():
            raise PermissionDenied("You don't have access to this object")
        return budget


class IncomeNode(DjangoObjectType):
    class Meta:
        model = Income
        filter_fields = ['amount', 'budget', 'transaction_date']
        interfaces = (relay.Node, )

    @classmethod
    @login_required
    def get_node(cls, info, id):
        income = super(IncomeNode, cls).get_node(info, id)
        if info.context.user not in income.budget.participants.all():
            raise PermissionDenied("You don't have access to this object")
        return income


class ExpanseNode(DjangoObjectType):
    class Meta:
        model = Expanse
        filter_fields = ['amount', 'budget', 'transaction_date']
        interfaces = (relay.Node, )

    @classmethod
    @login_required
    def get_node(cls, info, id):
        expanse = super(ExpanseNode, cls).get_node(info, id)
        if info.context.user not in expanse.budget.participants.all():
            raise PermissionDenied("You don't have access to this object")
        return expanse


class Query(graphene.ObjectType):
    budget = relay.Node.Field(BudgetNode)
    budgets = DjangoFilterConnectionField(BudgetNode)

    @login_required
    def resolve_budgets(self, info, **kwargs):
        return Budget.objects.filter(participants=info.context.user)

