from recipe.util import call_or_return_value, is_mutable


def test_call_or_return_value():
    def _func(arg1, arg2, arg3, kw1):
        return f'{kw1}: {arg1} {arg2} {arg3}'

    assert call_or_return_value('patate', 1, 2, 3, kw1='rogers') == 'patate'
    assert call_or_return_value(_func, 1, 2, 3, kw1='rogers') == 'rogers: 1 2 3'

def test_is_mutable():
    assert is_mutable([]) is True
    assert is_mutable({}) is True
    assert is_mutable(set()) is True
    assert is_mutable(frozenset()) is False
    assert is_mutable(str()) is False
    assert is_mutable(int()) is False
