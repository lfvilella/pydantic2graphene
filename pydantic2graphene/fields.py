import datetime
import typing
import ipaddress

import graphene
import graphene.types.datetime
import pydantic.fields

NOT_SUPPORTED_SHAPES = {
    pydantic.fields.SHAPE_MAPPING,
}

LIST_SHAPES = {
    pydantic.fields.SHAPE_LIST,
    pydantic.fields.SHAPE_TUPLE,
    pydantic.fields.SHAPE_TUPLE_ELLIPSIS,
    pydantic.fields.SHAPE_SEQUENCE,
    pydantic.fields.SHAPE_SET,
    pydantic.fields.SHAPE_FROZENSET,
    pydantic.fields.SHAPE_ITERABLE,
}

TYPE_MAPPING = {
    str: graphene.String,
    bool: graphene.Boolean,
    float: graphene.Float,
    int: graphene.Int,
    bytes: graphene.String,
    datetime.datetime: graphene.types.datetime.DateTime,
    typing.Pattern: graphene.String,
    ipaddress.IPv4Address: graphene.String,
    ipaddress.IPv4Interface: graphene.String,
    ipaddress.IPv4Network: graphene.String,
    ipaddress.IPv6Address: graphene.String,
    ipaddress.IPv6Interface: graphene.String,
    ipaddress.IPv6Network: graphene.String,
}
# graphene==1.X does not support Date
# graphene==2.X does not support Date
try:
    TYPE_MAPPING[datetime.date] = graphene.types.datetime.Date
except AttributeError:
    pass

# graphene==1.X does not support Time
try:
    TYPE_MAPPING[datetime.time] = graphene.types.datetime.Time
except AttributeError:
    pass


LIST_FIELDS_NOT_TYPED = {
    list,
    tuple,
    dict,
    set,
    frozenset,
}

graphene_type = typing.Union[
    graphene.ObjectType, graphene.InputObjectType, graphene.Interface,
]
