import pytest
from recipe.types_ import RecipeResult


def test_immutability_of_recipe_result():
    result = RecipeResult(actual_value='patate', last_value='Patate', error=None)

    with pytest.raises(AttributeError):
        result.actual_value = 'rogers'

    with pytest.raises(AttributeError):
        result.last_value = 'rogers'

    with pytest.raises(AttributeError):
        result.error = Exception('rogers')


def test_recipe_result_attributes_get():
    result = RecipeResult(actual_value='patate', last_value='Patate', error=None)

    assert result.actual_value == 'patate'
    assert result.last_value == 'Patate'
    assert result.error is None
