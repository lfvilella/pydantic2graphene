import datetime
import typing
import ipaddress
import enum
import decimal
import uuid
import inspect

import graphene
import graphene.types.datetime
import pydantic.fields

_NOT_SUPPORTED_SHAPES = {
    pydantic.fields.SHAPE_MAPPING,
}

_LIST_SHAPES = {
    pydantic.fields.SHAPE_LIST,
    pydantic.fields.SHAPE_TUPLE,
    pydantic.fields.SHAPE_TUPLE_ELLIPSIS,
    pydantic.fields.SHAPE_SEQUENCE,
    pydantic.fields.SHAPE_SET,
    pydantic.fields.SHAPE_FROZENSET,
    pydantic.fields.SHAPE_ITERABLE,
}

_TYPE_MAPPING = None


def _get_type_mapping():
    global _TYPE_MAPPING
    if _TYPE_MAPPING:
        return _TYPE_MAPPING

    _TYPE_MAPPING = {
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
        decimal.Decimal: graphene.Float,
        uuid.UUID: graphene.String,
        pydantic.EmailStr: graphene.String,
        pydantic.NameEmail: graphene.String,
        pydantic.color.Color: graphene.String,
        # pydantic.Json: graphene.types.json.JSONString,
        pydantic.HttpUrl: graphene.String,
        pydantic.UUID1: graphene.String,
        pydantic.UUID3: graphene.String,
        pydantic.UUID4: graphene.String,
        pydantic.UUID5: graphene.String,
        pydantic.SecretBytes: graphene.String,
        pydantic.SecretStr: graphene.String,
        pydantic.IPvAnyAddress: graphene.String,
        pydantic.IPvAnyInterface: graphene.String,
        pydantic.IPvAnyNetwork: graphene.String,
        pydantic.NegativeFloat: graphene.Float,
        pydantic.NegativeInt: graphene.Int,
        pydantic.PositiveFloat: graphene.Float,
        pydantic.PositiveInt: graphene.Int,
        pydantic.conbytes: graphene.String,
        pydantic.types.ConstrainedBytes: graphene.String,
        pydantic.condecimal: graphene.Float,
        pydantic.confloat: graphene.Float,
        pydantic.conint: graphene.Int,
        pydantic.constr: graphene.String,
        # pydantic.conlist: ,
    }

    # graphene does not support Date on versions:
    # ('1.X', '2.0')
    try:
        _TYPE_MAPPING[datetime.date] = graphene.types.datetime.Date
    except AttributeError:
        pass

    # graphene does not support Time on versions:
    # ('1.1.2', '1.1.1', '1.1', '1.0.2', '1.0.1', '1.0')
    try:
        _TYPE_MAPPING[datetime.time] = graphene.types.datetime.Time
    except AttributeError:
        pass

    # pydantic needs 'email-validator' to these fields
    try:
        _TYPE_MAPPING[pydantic.EmailStr] = graphene.String
        _TYPE_MAPPING[pydantic.NameEmail] = graphene.String
    except ImportError:
        pass

    return _TYPE_MAPPING


_LIST_FIELDS_NOT_TYPED = {
    list,
    tuple,
    dict,
    set,
    frozenset,
}


_ENUM_TYPE = (
    enum.Enum,
    enum.IntEnum,
)

_CONSTRAINED_TYPES = {
    pydantic.types.ConstrainedBytes,
    # pydantic.types.ConstrainedList,
    # pydantic.types.ConstrainedStr,
    # pydantic.types.ConstrainedInt,
    # pydantic.types.ConstrainedFloat,
    # pydantic.types.ConstrainedDecimal,

    # pydantic.types.ConstrainedSet,
    # pydantic.types.PositiveInt,
    # pydantic.types.NegativeInt,
    # pydantic.types.PositiveFloat,
    # pydantic.types.NegativeFloat,
    # pydantic.types.UUID1,
    # pydantic.types.UUID3,
    # pydantic.types.UUID4,
    # pydantic.types.UUID5,

    # 'Json',
    # pydantic.types.Json,
    # 'JsonWrapper',

    # pydantic.types.SecretStr,
    # pydantic.types.SecretBytes,
    # pydantic.types.StrictBool,
    # pydantic.types.StrictInt,
    # pydantic.types.StrictFloat,
    # pydantic.types.PaymentCardNumber,
    # pydantic.types.ByteSize,
}


def _extract_pydantic_base_type(type_):
    for super_class in type_.mro():
        if 'pydantic.types.' in repr(super_class):
            yield super_class


def get_grapehene_field_by_type(type_):
    mapping = _get_type_mapping()

    if type_ in mapping:
        return mapping[type_]

    if inspect.isclass(type_):
        for pydantic_type in _extract_pydantic_base_type(type_):
            if pydantic_type in mapping:
                return mapping[pydantic_type]


def is_field_not_allowed_type(type_) -> bool:
    return type_ in _LIST_FIELDS_NOT_TYPED


def is_enum_type(type_) -> bool:
    return inspect.isclass(type_) and issubclass(type_, _ENUM_TYPE)


def is_list_shape(shape) -> bool:
    return shape in _LIST_SHAPES


def is_not_supported_shape(shape) -> bool:
    return shape in _NOT_SUPPORTED_SHAPES


def is_pydantic_base_model(type_) -> bool:
    return inspect.isclass(type_) and issubclass(type_, pydantic.BaseModel)
