from recipe.recipe_core import Recipe
from recipe.tools import do, do_and_take_index, while_
from recipe.types_ import RecipeResult

test_changing_value = "germaine"


def _get_value(s: str) -> str:
    global test_changing_value
    value = test_changing_value
    test_changing_value = "gertrude"

    return s + value


recipe = Recipe(
    "test",
    do(str.lower),
    do_and_take_index(str.split, "-", _index=0),
    do(lambda x: x + " patate"),
    while_(do(lambda x: x[0:-1]), _condition=lambda x: len(x) > 2),
)


recipe_cache = Recipe(
    "test",
    do(str.lower),
    do_and_take_index(str.split, "-", _index=0),
    do(lambda x: x + " patate"),
    while_(do(lambda x: x[0:-1]), _condition=lambda x: len(x) > 2),
    do(_get_value),
)


recipe_not_cache = Recipe(
    "test",
    do(str.lower),
    do_and_take_index(str.split, "-", _index=0),
    do(lambda x: x + " patate"),
    while_(do(lambda x: x[0:-1]), _condition=lambda x: len(x) > 2),
    do(_get_value),
    cachable=False,
)


def test_recipe_normal_execution():
    result = recipe("ROGERS-BERTRAND")

    assert result is not None
    assert isinstance(result, RecipeResult)
    assert result.actual_value == "ro"
    assert result.last_value == "rogers patate"
    assert result.error is None

    result2 = recipe("ROGERS-BERTRAND")
    assert result == result2


def test_recipe_cache():
    result = recipe_cache("ROGERS-BERTRAND")
    result2 = recipe_cache("ROGERS-BERTRAND")

    assert (
        result == result2
    )  # but we know that value was changed in _get_value function, this proves the cache is working


def test_recipe_no_cache():
    global test_changing_value
    test_changing_value = "bernando"

    result = recipe_not_cache("ROGERS-BERTRAND")
    result2 = recipe_not_cache("ROGERS-BERTRAND")

    assert result != result2


def test_recipe_on_empty_initial_value():
    result = recipe("")

    assert result is not None
    assert isinstance(result, RecipeResult)
    assert result.actual_value == ""
    assert result.last_value == ""
    assert result.error is None


def test_recipe_on_none_initial_value():
    result = recipe(None)

    assert result is not None
    assert isinstance(result, RecipeResult)
    assert result.actual_value == ""
    assert result.last_value == ""
    assert result.error is None


def test_recipe_on_bad_initial_value():
    result = recipe(1)

    assert result is not None
    assert isinstance(result, RecipeResult)
    assert result.actual_value == 1
    assert result.last_value == 1
    assert str(result.error) == str(
        TypeError("descriptor 'lower' for 'str' objects doesn't apply to a 'int' object")
    )
