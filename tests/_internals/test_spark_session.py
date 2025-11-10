import pytest
from p3._internals import SessionEngine, SessionGenerator


def test_enumeration() -> None:
    with pytest.raises(ValueError):
        SessionGenerator(engine='arbitrary')


@pytest.mark.parametrize(
    ['key', 'value'],
    [
        ('DUCKDB', 1),
        ('REMOTE', 2),
        ('LOCAL', 3),
    ],
)
def test_enum(key, value) -> None:
    assert getattr(SessionEngine, key).value == value
