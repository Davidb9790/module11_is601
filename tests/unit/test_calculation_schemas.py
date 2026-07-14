import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.schemas.calculation import (
    CalculationCreate,
    CalculationBase,
    CalculationUpdate,
    CalculationResponse,
    CalculationType
)


# ---------------------------------------------------------
# Base Schema Validation
# ---------------------------------------------------------

def test_base_schema_valid():
    """Base schema should accept valid type and inputs."""
    schema = CalculationBase(type="addition", inputs=[10, 5])
    assert schema.type == CalculationType.ADDITION
    assert schema.inputs == [10, 5]


def test_base_schema_invalid_type():
    """Invalid type should raise ValidationError."""
    with pytest.raises(ValidationError):
        CalculationBase(type="invalid", inputs=[10, 5])


def test_base_schema_not_enough_inputs():
    """Less than 2 inputs should raise ValidationError."""
    with pytest.raises(ValidationError):
        CalculationBase(type="addition", inputs=[10])


def test_base_schema_division_by_zero():
    """Division with zero denominator should raise ValidationError."""
    with pytest.raises(ValidationError):
        CalculationBase(type="division", inputs=[100, 0])


# ---------------------------------------------------------
# CalculationCreate Validation
# ---------------------------------------------------------

def test_create_schema_valid():
    """Valid CalculationCreate should pass."""
    user_id = uuid4()
    schema = CalculationCreate(type="addition", inputs=[1, 2], user_id=user_id)
    assert schema.user_id == user_id


def test_create_missing_user_id():
    """Missing user_id should raise ValidationError."""
    with pytest.raises(ValidationError):
        CalculationCreate(type="addition", inputs=[1, 2])


def test_create_invalid_type():
    """Invalid type should raise ValidationError."""
    with pytest.raises(ValidationError):
        CalculationCreate(type="invalid", inputs=[1, 2], user_id=uuid4())


def test_create_division_by_zero():
    """Division by zero should raise ValidationError."""
    with pytest.raises(ValidationError):
        CalculationCreate(type="division", inputs=[10, 0], user_id=uuid4())


# ---------------------------------------------------------
# CalculationUpdate Validation
# ---------------------------------------------------------

def test_update_schema_valid():
    """Update schema should accept valid inputs."""
    schema = CalculationUpdate(inputs=[10, 5])
    assert schema.inputs == [10, 5]


def test_update_schema_not_enough_inputs():
    """Update schema should reject invalid input length."""
    with pytest.raises(ValidationError):
        CalculationUpdate(inputs=[10])


def test_update_schema_none_inputs():
    """None inputs should be allowed (partial update)."""
    schema = CalculationUpdate(inputs=None)
    assert schema.inputs is None


# ---------------------------------------------------------
# CalculationResponse Validation
# ---------------------------------------------------------

def test_response_schema_valid():
    """Response schema should accept all required fields."""
    user_id = uuid4()
    calc_id = uuid4()

    schema = CalculationResponse(
        id=calc_id,
        user_id=user_id,
        type="addition",
        inputs=[1, 2],
        result=3,
        created_at="2025-01-01T00:00:00",
        updated_at="2025-01-01T00:00:00",
    )

    assert schema.id == calc_id
    assert schema.user_id == user_id
    assert schema.result == 3
    assert schema.type == CalculationType.ADDITION