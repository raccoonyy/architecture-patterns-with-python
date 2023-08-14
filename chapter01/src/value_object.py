from collections import namedtuple
from copy import deepcopy
from dataclasses import dataclass
from typing import NamedTuple

import pytest


@dataclass(frozen=True)
class Name:
    first_name: str
    sur_name: str


class Money(NamedTuple):
    currency: str
    value: int


Line = namedtuple('Line', ['sku', 'qty'])


def test_동등성():
    assert Money('gbp', 10) == Money('gbp', 10)
    assert Name('Harry', 'Percival') != Name('Bob', 'Gregory')
    assert Line('RED-CHAIR', 5) == Line('RED-CHAIR', 5)


fiver = Money('gbp', 5)
tenner = Money('gbp', 10)


def test_화폐가_같으면_더할_수_있다():
    assert fiver + fiver == tenner


def test_Money끼리는_뺄_수_있다():
    assert tenner - fiver == fiver


def test_화폐가_다르면_더하기_실패():
    with pytest.raises(ValueError):
        Money('usd', 10) + Money('gbp', 10)


def test_Money는_숫자와_곱할_수_있다():
    assert fiver * 5 == Money('gbp', 25)


def test_Money끼리는_곱할_수_없다():
    with pytest.raises(TypeError):
        tenner * fiver


class Person:
    def __init__(self, name: Name):
        self.name = name

    def __eq__(self, other: "Person"):
        return self.name == other.name


def test_barry는_harry다():
    harry = Person(Name('Harry', 'Percival'))
    barry = deepcopy(harry)

    # barry.name = Name('Barry', 'Percival')

    assert harry == barry and barry == harry
    assert harry is not barry
