from typing import Iterable

import pytest
import logging

from recipe.on_error import OnError
from recipe.tools import do, do_and_take_index, while_, if_


def test_do():
    def _func(s: str, length: int = 4) -> str:
        return s[0:length]

    def _raiser(s: str, length: int = 4) -> str:
        raise Exception('test')

    first = do(str.upper)
    second_default = do(_func)
    second_with_arg = do(_func, 2)
    second_with_kwarg = do(_func, length=5)
    raiser = do(_raiser)

    assert first is not None
    assert second_default is not None
    assert second_with_arg is not None
    assert second_with_kwarg is not None

    assert getattr(first, '__real_name__', None) == 'str.upper'
    assert getattr(second_default, '__real_name__', None) == 'test_do.<locals>._func'
    assert getattr(second_with_arg, '__real_name__', None) == 'test_do.<locals>._func'
    assert getattr(second_with_kwarg, '__real_name__', None) == 'test_do.<locals>._func'

    assert first('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.LOG) == 'ROGERS-POTATO'
    assert second_default('ROGERS-POTATO', 'sequence', logging.getLogger(), OnError.LOG) == 'ROGE'
    assert second_with_arg('ROGERS-POTATO', 'sequence', logging.getLogger(), OnError.LOG) == 'RO'
    assert second_with_kwarg('ROGERS-POTATO', 'sequence', logging.getLogger(), OnError.LOG) == 'ROGER'

    with pytest.raises(Exception):
        raiser('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.LOG)


def test_do_and_take_index():
    def _func(l: Iterable) -> Iterable:
        return l

    def _raiser(l: Iterable) -> Iterable:
        raise Exception('test')

    func_first = do_and_take_index(_func, _index=0)
    func_third = do_and_take_index(_func, _index=2)
    func_last = do_and_take_index(_func, _index=-1)
    raiser = do_and_take_index(_raiser, _index=0)

    assert func_first([1, 2, 3, 4, 5], 'sequence', logging.getLogger(), OnError.LOG) == 1
    assert func_third([1, 2, 3, 4, 5], 'sequence', logging.getLogger(), OnError.LOG) == 3
    assert func_last([1, 2, 3, 4, 5], 'sequence', logging.getLogger(), OnError.LOG) == 5

    with pytest.raises(Exception):
        raiser([1, 2, 3, 4, 5], 'sequence', logging.getLogger(), OnError.LOG)


def test_while():
    def _crop(s: str, how_much: int) -> str:
        return s[0:-how_much]

    def _add(s: str, what: str) -> str:
        return s + what

    def _raiser(s: str):
        raise Exception('test')

    while_empty = while_(
        do(_crop, how_much=2),
        do(_add, what='-'),
        _block_name='test'
    )

    while_condition = while_(
        do(_crop, how_much=2),
        do(_add, what='-'),
        _block_name='test2',
        _condition=lambda s: len(s) > 5
    )

    while_error = while_(
        do(_crop, how_much=2),
        do(_add, what='-'),
        do(_raiser),
        _block_name='test3'
    )

    assert while_empty('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.LOG) == '-'
    assert while_condition('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.LOG) == 'roge-'

    assert while_error('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.LOG) == '-'

    with pytest.raises(Exception):
        while_error('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.RAISE)


def test_if():
    def _on_true(s: str) -> str:
        return s + ' patate'

    def _on_false(s: str) -> str:
        return s + ' rogers'

    def _raiser(s: str) -> str:
        raise Exception('test')

    if_true = if_(
        True,
        _on_true=[
            do(_on_true)
        ],
        _on_false=[
            do(_on_false)
        ],
        _block_name='test1'
    )

    if_false = if_(
        False,
        _on_true=[
            do(_on_true)
        ],
        _on_false=[
            do(_on_false)
        ],
        _block_name='test2'
    )

    if_raiser = if_(
        True,
        _on_true=[
            do(_raiser)
        ],
        _block_name='test3'
    )

    assert if_true('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.LOG) == 'rogers-PoTatO patate'
    assert if_false('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.LOG) == 'rogers-PoTatO rogers'

    assert if_raiser('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.LOG) == 'rogers-PoTatO'
    with pytest.raises(Exception):
        if_raiser('rogers-PoTatO', 'sequence', logging.getLogger(), OnError.RAISE)
