import graphene
from django.db.models import AutoField, ForeignKey, ManyToManyField
from graphene import relay
from graphene_django.forms.mutation import DjangoModelFormMutation, DjangoFormMutation
from graphene_django.rest_framework.mutation import SerializerMutationOptions
from graphql_relay import from_global_id


class DjangoModelFormRelayMutation(DjangoModelFormMutation):
    class Meta:
        abstract = True

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        model = cls._meta.form_class._meta.model
        for field, value in input.items():
            if not hasattr(model, field):
                continue

            model_field = model._meta.get_field(field)
            if isinstance(model_field, (AutoField, ForeignKey)):
                _, input[field] = from_global_id(value)
            elif isinstance(model_field, ManyToManyField):
                input[field] = [int(from_global_id(value)[1] )for value in input[field]]

        return super().mutate_and_get_payload(root, info, **input)


class RelayClientIdDeleteMutation(relay.ClientIDMutation):
    id = graphene.ID()
    message = graphene.String()

    class Input:
        id = graphene.ID(required=True)

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
            cls,
            model_class=None,
            **options
    ):
        _meta = SerializerMutationOptions(cls)
        _meta.model_class = model_class
        super(RelayClientIdDeleteMutation, cls).__init_subclass_with_meta__(
            _meta=_meta, **options
        )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        id = int(from_global_id(id)[1])
        cls.get_queryset(cls._meta.model_class.objects.all(),
                         info).get(id=id).delete()
        return cls(id=id, message='deleted')