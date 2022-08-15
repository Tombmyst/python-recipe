import logging
import operator
from typing import Any

from recipe.on_error import OnError
from recipe.recipe_core import execute_sequence_of_functions
from recipe.tools import do
from recipe.types_ import RecipeResult


def test_execute_sequence_of_functions_with_string():
    functions = [do(str.strip), do(str.upper), do(str.replace, " ", "-")]

    result: RecipeResult = execute_sequence_of_functions(
        sequence_name="test",
        tool_functions=functions,
        initial_value="  hello world  ",
        logger=logging.getLogger(),
        on_error=OnError.IGNORE,
    )

    assert result is not None
    assert isinstance(result, RecipeResult)
    assert result.actual_value == "HELLO-WORLD"
    assert result.last_value == "HELLO WORLD"
    assert result.error is None


def test_execute_sequence_of_functions_with_int():
    functions = [do(operator.add, 3), do(operator.mul, 2), do(operator.sub, 1)]

    result: RecipeResult = execute_sequence_of_functions(
        sequence_name="test",
        tool_functions=functions,
        initial_value=1,
        logger=logging.getLogger(),
        on_error=OnError.IGNORE,
    )

    assert result is not None
    assert isinstance(result, RecipeResult)
    assert result.actual_value == 7
    assert result.last_value == 8
    assert result.error is None


def test_execute_sequence_of_functions_with_list():
    def _append(value: list, item: Any) -> list:
        value.append(item)
        return value

    def _extend(value: list, items: list) -> list:
        value.extend(items)
        return value

    functions = [do(_append, "a"), do(_extend, ["b", "c"])]
    initial = ["d"]

    result: RecipeResult = execute_sequence_of_functions(
        sequence_name="test",
        tool_functions=functions,
        initial_value=initial,
        logger=logging.getLogger(),
        on_error=OnError.IGNORE,
        value_is_mutable=True,
    )

    assert result is not None
    assert isinstance(result, RecipeResult)
    assert result.actual_value == ["d", "a", "b", "c"]
    assert result.last_value == ["d", "a"]
    assert result.error is None
    assert initial == ["d"]


def test_execute_sequence_of_functions_with_none_as_input():
    functions = [do(str.strip), do(str.upper), do(str.replace, " ", "-")]

    result: RecipeResult = execute_sequence_of_functions(
        sequence_name="test",
        tool_functions=functions,
        initial_value=None,
        logger=logging.getLogger(),
        on_error=OnError.IGNORE,
    )

    assert result is not None
    assert isinstance(result, RecipeResult)
    assert result.actual_value is None
    assert result.last_value is None
    assert str(result.error) == str(
        TypeError("descriptor 'strip' for 'str' objects doesn't apply to a 'NoneType' object")
    )
