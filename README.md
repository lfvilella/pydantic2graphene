# pydantic2graphene

[![CI](https://github.com/lfvilella/pydantic2graphene/workflows/CI/badge.svg?event=push)](https://github.com/lfvilella/pydantic2graphene/actions?query=event%3Apush+branch%3Amaster+workflow%3ACI)
[![Forwards Compatibility](https://github.com/lfvilella/pydantic2graphene/workflows/Forwards%20Compatibility/badge.svg?event=schedule)](https://github.com/lfvilella/pydantic2graphene/actions?query=event:schedule+branch:master+workflow:Forwards%20Compatibility)
[![Coverage](https://codecov.io/gh/lfvilella/pydantic2graphene/branch/master/graph/badge.svg)](https://codecov.io/gh/lfvilella/pydantic2graphene)
[![pypi](https://img.shields.io/pypi/v/pydantic2graphene.svg)](https://pypi.python.org/pypi/pydantic2graphene)
[![versions](https://img.shields.io/pypi/pyversions/pydantic2graphene.svg)](https://github.com/lfvilella/pydantic2graphene)
[![license](https://img.shields.io/github/license/lfvilella/pydantic2graphene.svg)](https://github.com/lfvilella/pydantic2graphene/blob/master/LICENSE)

Easy way to convert pydantic2graphene models to graphene objects.


## A Simple Example

Using `to_graphene`

```py
import pydantic
import pydantic2graphene

class User(pydantic.BaseModel):
    email: str
    active: bool = False

UserGql = pydantic2graphene.to_graphene(User)
```

Converting to multiple graphene types with `ConverterToGrapheneBase`

```py
import pydantic
import pydantic2graphene

class User(pydantic.BaseModel):
    email: str
    active: bool = False

class UserConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = User

UserGql = UserConverter.as_class()  # graphene.ObjectType
UserInputGql = UserConverter.as_class(graphene.InputObjectType)
UserInterfaceGql = UserConverter.as_class(graphene.Interface)
```

[More Examples](https://github.com/lfvilella/pydantic2graphene/tree/master/docs/examples)
