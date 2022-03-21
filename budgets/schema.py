import graphene
from django.core.exceptions import PermissionDenied
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from budgets.filters import IncomeFilterSet, ExpanseFilterSet
from budgets.models import Budget, ExpanseCategory, Income, Expanse, BudgetParticipant


class ExpanseCategoryNode(DjangoObjectType):
    expanses_sum = graphene.Decimal(source='expanses_sum')

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
    incomes_sum = graphene.Decimal(source='incomes_sum')
    expanses_sum = graphene.Decimal(source='expanses_sum')
    incomes = DjangoFilterConnectionField('budgets.schema.IncomeNode', filterset_class=IncomeFilterSet)
    expanses = DjangoFilterConnectionField('budgets.schema.ExpanseNode', filterset_class=ExpanseFilterSet)

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


class BudgetParticipantNode(DjangoObjectType):
    participant = graphene.Field('users.schema.BaseUserNode', required=True)

    class Meta:
        model = BudgetParticipant
        filter_fields = ['participant', 'budget', 'is_owner']
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    budget = relay.Node.Field(BudgetNode)
    budgets = DjangoFilterConnectionField(BudgetNode)

    expanses_categories = DjangoFilterConnectionField(ExpanseCategoryNode)

    @login_required
    def resolve_budgets(self, info, **kwargs):
        return Budget.objects.filter(participants=info.context.user)

    @login_required
    def resolve_expanses_categories(self, info, **kwargs):
        return ExpanseCategory.objects.filter(budget__participants=info.context.user)

