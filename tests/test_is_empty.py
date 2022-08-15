from recipe.util import is_empty


def test_is_empty():
    assert is_empty("patate") is False
    assert is_empty("") is True
    assert is_empty(str()) is True

    assert is_empty({"patate"}) is False
    assert is_empty({"patate": "roger"}) is False
    assert is_empty(frozenset({"patate"})) is False
    assert is_empty({}) is True
    assert is_empty(dict()) is True
    assert is_empty(frozenset()) is True
    assert is_empty(set()) is True

    assert is_empty(("patate",)) is False
    assert is_empty(tuple()) is True
    assert is_empty(()) is True

    assert is_empty(["patate"]) is False
    assert is_empty([]) is True
    assert is_empty(list()) is True

    assert is_empty(0) is False
    assert is_empty(10) is False
    assert is_empty(None) is True
