from django.db.models import AutoField, ForeignKey, ManyToManyField
from graphene_django.forms.mutation import DjangoModelFormMutation, DjangoFormMutation
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
