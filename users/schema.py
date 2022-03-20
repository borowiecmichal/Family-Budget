from graphene import relay
from graphene_django import DjangoObjectType
from users.models import BaseUser


class BaseUserNode(DjangoObjectType):
    class Meta:
        model = BaseUser
        filter_fields = ['username', ]
        interfaces = (relay.Node, )
