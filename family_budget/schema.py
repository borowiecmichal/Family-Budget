import graphene

from graphql_auth.schema import UserQuery, MeQuery
from users.mutations import Mutations as UserMutations
from budgets.mutations import Mutations as BudgetMutations
from budgets.schema import Query as BudgetQuery


class Query(
    UserQuery,
    MeQuery,
    BudgetQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    UserMutations,
    BudgetMutations,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
