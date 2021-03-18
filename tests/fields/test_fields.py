import typing
import ipaddress
import enum
import decimal
import uuid
import datetime
import pathlib

import pytest
import pydantic
import pydantic2graphene
import graphene


def to_pydantic_class(field_type):
    class Fake(pydantic.BaseModel):
        field: field_type

    return Fake


class TestTypeMappingPydantic2Graphene:
    def test_bytes_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(bytes))
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_list_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(list))

    def test_tuple_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(tuple))

    def test_dict_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(dict))

    def test_set_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(set))

    def test_frozenset_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(frozenset))

    def test_datetime_date_field(self, normalize_sdl):
        version_1_x = graphene.__version__.startswith("1.")
        version_2_0 = graphene.__version__ == "2.0"
        if version_1_x or version_2_0:
            with pytest.raises(pydantic2graphene.FieldNotSupported):
                pydantic2graphene.to_graphene(to_pydantic_class(datetime.date))
            return

        value = pydantic2graphene.to_graphene(to_pydantic_class(datetime.date))
        expected_value = """
            scalarDatetypeFakeGql {
                field: Date!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_datetime_datetime_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(datetime.datetime)
        )
        expected_value = """
            scalarDateTimetypeFakeGql {
                field: DateTime!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_datetime_time_field(self, normalize_sdl):
        versions_1_x = {"1.1.2", "1.1.1", "1.1", "1.0.2", "1.0.1", "1.0"}
        if graphene.__version__ in versions_1_x:
            with pytest.raises(pydantic2graphene.FieldNotSupported):
                pydantic2graphene.to_graphene(to_pydantic_class(datetime.time))
            return

        value = pydantic2graphene.to_graphene(to_pydantic_class(datetime.time))
        expected_value = """
            type FakeGql {
                field: Time!
            }scalarTime
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_datetime_timedelta_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(datetime.timedelta)
            )

    def test_any_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(typing.Any))

    def test_type_var_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(typing.TypeVar("custom_types"))
            )

    def test_optional_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Optional[int])
        )
        expected_value = """
            type FakeGql {
                field: Int
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_list_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.List[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_tuple_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Tuple[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_dict_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(typing.Dict[str, str])
            )

    def test_typing_set_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Set[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_frozenset_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.FrozenSet[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_sequence_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Sequence[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_iterable_field(self, normalize_sdl):
        not_supported = str(pydantic.VERSION)[:3] in {
            "1.3",
            "1.2",
            "1.1",
            "1.0",
        }
        if not_supported:
            with pytest.raises(pydantic2graphene.FieldNotSupported):
                pydantic2graphene.to_graphene(
                    to_pydantic_class(typing.Type[str])
                )
            return

        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Iterable[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_type_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(typing.Type[str]))

    def test_typing_callable_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(typing.Callable[[int], str])
            )

    def test_typing_pattern_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Pattern)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_ipaddress_ipv4address_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(ipaddress.IPv4Address)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_ipaddress_ipv4interface_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(ipaddress.IPv4Interface)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_ipaddress_ipv4network_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(ipaddress.IPv4Network)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_ipaddress_ipv6address_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(ipaddress.IPv6Address)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_ipaddress_ipv6interface_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(ipaddress.IPv6Interface)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_ipaddress_ipv6network_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(ipaddress.IPv6Network)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_enum_field(self, normalize_sdl):
        class EnumTest(enum.Enum):
            ONE = 1
            TWO = 2

        value = pydantic2graphene.to_graphene(to_pydantic_class(EnumTest))
        expected_value = """
            enum EnumTest {
                ONE
                TWO
            }

            type FakeGql {
                field: EnumTest!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_int_enum_field(self, normalize_sdl):
        class Enumer(enum.IntEnum):
            ONE = 1
            TWO = 2

        value = pydantic2graphene.to_graphene(to_pydantic_class(Enumer))
        expected_value = """
            enum Enumer {
                ONE
                TWO
            }

            type FakeGql {
                field: Enumer!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_decimal_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(decimal.Decimal)
        )
        expected_value = """
            type FakeGql {
                field: Float!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pathlib_path_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(pathlib.Path))

    def test_uuid_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(uuid.UUID))
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_filepath_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(pydantic.FilePath))

    def test_pydantic_directorypath_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(pydantic.DirectoryPath)
            )

    def test_pydantic_pyobject_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(pydantic.PyObject))

    def test_pydantic_color_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.color.Color)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_json_field(self, normalize_sdl):
        graphene_not_suported = graphene.__version__ in {
            "1.4.2",
            "1.4.1",
            "1.4",
            "1.3",
            "1.2",
            "1.1.3",
            "1.1.2",
            "1.1.1",
            "1.1",
            "1.0.2",
            "1.0.1",
            "1.0",
        }
        pydantic_not_supported = str(pydantic.VERSION)[:3] in {
            "1.2",
            "1.1",
            "1.0",
        }
        if graphene_not_suported or pydantic_not_supported:
            with pytest.raises(pydantic2graphene.FieldNotSupported):
                pydantic2graphene.to_graphene(to_pydantic_class(pydantic.Json))
            return

        value = pydantic2graphene.to_graphene(to_pydantic_class(pydantic.Json))
        expected_value = """
            type FakeGql {
                field: JSONString
            }

            scalar JSONString
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_payment_card_number_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.PaymentCardNumber)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_any_url_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.AnyUrl)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_any_http_url_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.AnyHttpUrl)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_http_url_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.HttpUrl)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_postgresdsn_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.PostgresDsn)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_redisdsn_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.RedisDsn)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_stricturl_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.stricturl())
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_uuid1_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.UUID1)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_uuid3_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.UUID3)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_uuid4_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.UUID4)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_uuid5_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.UUID5)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_secret_bytes_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.SecretBytes)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_secret_str_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.SecretStr)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_ipv_any_address_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.IPvAnyAddress)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_ipv_any_interface_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.IPvAnyInterface)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_ipv_any_network_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.IPvAnyNetwork)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_negative_float_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.NegativeFloat)
        )
        expected_value = """
            type FakeGql {
                field: Float!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_negative_int_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.NegativeInt)
        )
        expected_value = """
            type FakeGql {
                field: Int!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_positive_float_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.PositiveFloat)
        )
        expected_value = """
            type FakeGql {
                field: Float!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_positive_int_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.PositiveInt)
        )
        expected_value = """
            type FakeGql {
                field: Int!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_conbytes_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.conbytes())
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_condecimal_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.condecimal())
        )
        expected_value = """
            type FakeGql {
                field: Float!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_confloat_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.confloat())
        )
        expected_value = """
            type FakeGql {
                field: Float!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_conint_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.conint())
        )
        expected_value = """
            type FakeGql {
                field: Int!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_conlist_int_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.conlist(int, min_items=1, max_items=4))
        )
        expected_value = """
            type FakeGql {
                field: [Int!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_conlist_str_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.conlist(str, min_items=1, max_items=4))
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_conset_int_field(self, normalize_sdl):
        not_implemented = str(pydantic.VERSION)[:3] in {
            "1.5",
            "1.4",
            "1.3",
            "1.2",
            "1.1",
            "1.0",
        }
        if not_implemented:
            # AttributeError: module 'pydantic' has no attribute 'conset'
            # Pydantic versions < 1.6 return error when using conset
            return

        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.conset(int, min_items=1, max_items=4))
        )
        expected_value = """
            type FakeGql {
                field: [Int!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_conset_str_field(self, normalize_sdl):
        not_implemented = str(pydantic.VERSION)[:3] in {
            "1.5",
            "1.4",
            "1.3",
            "1.2",
            "1.1",
            "1.0",
        }
        if not_implemented:
            # AttributeError: module 'pydantic' has no attribute 'conset'
            # Pydantic versions < 1.6 return error when using conset
            return

        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.conset(str, min_items=1, max_items=4))
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_constr_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.constr())
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    @pytest.mark.parametrize('base_type, graphene_type_name', (
        (str, 'String'),
        (int, 'Int'),
        (float, 'Float'),
        (decimal.Decimal, 'Float'),
        (bytes, 'String'),
    ))
    def test_subclass_of_supported_fields(self, normalize_sdl, base_type, graphene_type_name):
        class MyCustomSubclass(base_type):
            pass

        value = pydantic2graphene.to_graphene(
            to_pydantic_class(MyCustomSubclass)
        )
        expected_value = """
            type FakeGql {
                field: %s!
            }
        """ % graphene_type_name
        assert normalize_sdl(value) == normalize_sdl(expected_value)
