import graphene

from graphql_auth.schema import UserQuery, MeQuery
from users.mutations import Mutations as UsersMutations


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(UsersMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
