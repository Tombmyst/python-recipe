import pytest

from recipe.types_ import NULL


def test_null_type():
    assert NULL == NULL
    assert NULL is NULL
    assert NULL is not None
    assert NULL != None

    if NULL:
        pytest.xfail("Should not occur")

    assert str(NULL) == repr(NULL) == "NULL"
    assert len(NULL) == 0
    assert bool(NULL) is False
