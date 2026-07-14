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
# Subclass Instantiation Tests
# ---------------------------------------------------------

def test_addition_model():
    """Addition model should compute correct result."""
    calc = Addition(user_id=uuid4(), inputs=[2, 3, 5])
    assert calc.get_result() == 10


def test_subtraction_model():
    """Subtraction model should compute correct result."""
    calc = Subtraction(user_id=uuid4(), inputs=[10, 3, 2])
    assert calc.get_result() == 5


def test_multiplication_model():
    """Multiplication model should compute correct result."""
    calc = Multiplication(user_id=uuid4(), inputs=[2, 3, 4])
    assert calc.get_result() == 24


def test_division_model():
    """Division model should compute correct result."""
    calc = Division(user_id=uuid4(), inputs=[100, 2, 5])
    assert calc.get_result() == 10


def test_division_by_zero_model():
    """Division model should raise ValueError when dividing by zero."""
    calc = Division(user_id=uuid4(), inputs=[10, 0])
    with pytest.raises(ValueError):
        calc.get_result()


# ---------------------------------------------------------
# Polymorphic Identity Tests
# ---------------------------------------------------------

def test_polymorphic_identity_addition():
    """Addition model should have correct polymorphic identity."""
    calc = Addition(user_id=uuid4(), inputs=[1, 2])
    assert calc.type == "addition"


def test_polymorphic_identity_subtraction():
    calc = Subtraction(user_id=uuid4(), inputs=[1, 2])
    assert calc.type == "subtraction"


def test_polymorphic_identity_multiplication():
    calc = Multiplication(user_id=uuid4(), inputs=[1, 2])
    assert calc.type == "multiplication"


def test_polymorphic_identity_division():
    calc = Division(user_id=uuid4(), inputs=[1, 2])
    assert calc.type == "division"


# ---------------------------------------------------------
# Base Class Behavior
# ---------------------------------------------------------

def test_base_class_fields():
    """Base Calculation class should store user_id and inputs."""
    calc = Calculation(user_id=uuid4(), inputs=[10, 20])
    assert calc.inputs == [10, 20]
    assert isinstance(calc.user_id, uuid4().__class__)


# ---------------------------------------------------------
# Factory + Model Integration
# ---------------------------------------------------------

def test_factory_and_model_logic():
    """Factory should create correct subclass and compute correct result."""
    calc = Calculation.create("multiplication", uuid4(), [2, 3, 4])
    assert isinstance(calc, Multiplication)
    assert calc.get_result() == 24
