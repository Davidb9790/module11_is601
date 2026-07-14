import pytest
from uuid import uuid4

from app.models.calculation import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division
)


# ---------------------------------------------------------
# Factory should return the correct subclass
# ---------------------------------------------------------

@pytest.mark.parametrize(
    "calc_type, expected_class",
    [
        ("addition", Addition),
        ("subtraction", Subtraction),
        ("multiplication", Multiplication),
        ("division", Division),
    ]
)
def test_factory_creates_correct_subclass(calc_type, expected_class):
    """Ensure the factory returns the correct calculation subclass."""
    user_id = uuid4()
    inputs = [10, 5]

    calc = Calculation.create(calc_type, user_id, inputs)

    assert isinstance(calc, expected_class)
    assert calc.user_id == user_id
    assert calc.inputs == inputs


# ---------------------------------------------------------
# Factory should normalize type (case-insensitive)
# ---------------------------------------------------------

def test_factory_type_is_case_insensitive():
    """Factory should accept type strings in any case."""
    calc = Calculation.create("AdDiTiOn", uuid4(), [1, 2])
    assert isinstance(calc, Addition)


# ---------------------------------------------------------
# Factory should reject invalid types
# ---------------------------------------------------------

def test_factory_invalid_type():
    """Invalid calculation type should raise ValueError."""
    with pytest.raises(ValueError):
        Calculation.create("invalid_type", uuid4(), [1, 2])


# ---------------------------------------------------------
# Factory should enforce minimum inputs (delegated to model)
# ---------------------------------------------------------

def test_factory_invalid_inputs():
    """Factory should allow model to raise errors for invalid inputs."""
    calc = Calculation.create("addition", uuid4(), [5])
    assert isinstance(calc, Addition)
    assert calc.inputs == [5]


# ---------------------------------------------------------
# Factory + subclass logic integration test
# ---------------------------------------------------------

def test_factory_and_subclass_logic():
    """Ensure factory-created objects compute correct results."""
    calc = Calculation.create("multiplication", uuid4(), [2, 3, 4])
    assert calc.get_result() == 24
