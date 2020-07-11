import typing
import graphene

GrapheneObjectType = typing.Union[
    graphene.ObjectType, graphene.InputObjectType, graphene.Interface,
]

GrapheneField = typing.TypeVar("graphene.BaseType")
