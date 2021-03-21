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


_NOT_SUPPORTED_SHAPES = None


def _get_not_supported_shapes():
    global _NOT_SUPPORTED_SHAPES
    if _NOT_SUPPORTED_SHAPES:
        return _NOT_SUPPORTED_SHAPES

    _NOT_SUPPORTED_SHAPES = {
        pydantic.fields.SHAPE_MAPPING,
    }

    # pydantic pydantic<=1.8 does not have SHAPE_DICT and SHAPE_DEFAULTDICT
    try:
        _NOT_SUPPORTED_SHAPES.add(pydantic.fields.SHAPE_DICT)
        _NOT_SUPPORTED_SHAPES.add(pydantic.fields.SHAPE_DEFAULTDICT)
    except AttributeError:
        pass

    return _NOT_SUPPORTED_SHAPES


_LIST_SHAPES = None


def _get_list_shapes():
    global _LIST_SHAPES
    if _LIST_SHAPES:
        return _LIST_SHAPES

    _LIST_SHAPES = {
        pydantic.fields.SHAPE_LIST,
        pydantic.fields.SHAPE_TUPLE,
        pydantic.fields.SHAPE_TUPLE_ELLIPSIS,
        pydantic.fields.SHAPE_SEQUENCE,
        pydantic.fields.SHAPE_SET,
        pydantic.fields.SHAPE_FROZENSET,
    }

    # pydantic pydantic<=1.3 does not have SHAPE_ITERABLE
    try:
        _LIST_SHAPES.add(pydantic.fields.SHAPE_ITERABLE)
    except AttributeError:
        pass

    return _LIST_SHAPES


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
        pydantic.PaymentCardNumber: graphene.String,
        pydantic.AnyUrl: graphene.String,
        pydantic.AnyHttpUrl: graphene.String,
        pydantic.HttpUrl: graphene.String,
        pydantic.PostgresDsn: graphene.String,
        pydantic.RedisDsn: graphene.String,
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
        pydantic.types.ConstrainedDecimal: graphene.Float,
        pydantic.confloat: graphene.Float,
        pydantic.types.ConstrainedFloat: graphene.Float,
        pydantic.conint: graphene.Int,
        pydantic.types.ConstrainedInt: graphene.Int,
        pydantic.constr: graphene.String,
        pydantic.types.ConstrainedStr: graphene.String,
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

    # graphene does not support JSONString on versions:
    # ( 1.0>=, <=1.4.2 )
    try:
        _TYPE_MAPPING[pydantic.Json] = graphene.types.json.JSONString
    except AttributeError:
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


def get_grapehene_field_by_type(type_):
    mapping = _get_type_mapping()

    if type_ in mapping:
        return mapping[type_]

    if inspect.isclass(type_):
        for pydantic_type in type_.mro():
            if pydantic_type in mapping:
                return mapping[pydantic_type]


def is_field_not_allowed_type(type_) -> bool:
    return type_ in _LIST_FIELDS_NOT_TYPED


def is_enum_type(type_) -> bool:
    return inspect.isclass(type_) and issubclass(type_, _ENUM_TYPE)


def is_list_shape(shape) -> bool:
    return shape in _get_list_shapes()


def is_not_supported_shape(shape) -> bool:
    return shape in _get_not_supported_shapes()


def is_pydantic_base_model(type_) -> bool:
    return inspect.isclass(type_) and issubclass(type_, pydantic.BaseModel)


def is_graphene_type(type_) -> bool:
    return "graphene.types" in repr(type_)
