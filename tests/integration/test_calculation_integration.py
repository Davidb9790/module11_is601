# import pytest
# from uuid import uuid4
# from sqlalchemy.orm import Session

# from app.database import get_engine, get_sessionmaker, Base
# from app.models.calculation import Calculation, Addition, Division
# from app.schemas.calculation import CalculationCreate
# from pydantic import ValidationError


# # ---------------------------------------------------------
# # Database Session Fixture (real PostgreSQL)
# # ---------------------------------------------------------

# @pytest.fixture(scope="module")
# def db_session():
#     """
#     Creates a real database session using the DATABASE_URL from settings.
#     This runs against the PostgreSQL container in GitHub Actions.
#     """
#     engine = get_engine()  # uses settings.DATABASE_URL
#     print("DATABASE_URL:", engine.url)
#     Base.metadata.create_all(bind=engine)

#     TestingSessionLocal = get_sessionmaker(engine)
#     session = TestingSessionLocal()

#     yield session

#     session.close()
#     Base.metadata.drop_all(bind=engine)


# # ---------------------------------------------------------
# # Insert + Retrieve Test
# # ---------------------------------------------------------

# def test_insert_calculation_record(db_session: Session):
#     """Insert a calculation record and confirm DB stores correct data."""
#     calc = Addition(user_id=uuid4(), inputs=[10, 5])

#     db_session.add(calc)
#     db_session.commit()
#     db_session.refresh(calc)

#     stored = db_session.query(Calculation).filter_by(id=calc.id).first()

#     assert stored is not None
#     assert stored.type == "addition"
#     assert stored.inputs == [10, 5]
#     assert stored.get_result() == 15


# # ---------------------------------------------------------
# # Invalid Type (Schema Validation)
# # ---------------------------------------------------------

# def test_invalid_type_schema():
#     """Invalid type should raise ValidationError before DB insert."""
#     with pytest.raises(ValidationError):
#         CalculationCreate(type="invalid", inputs=[1, 2], user_id=uuid4())


# # ---------------------------------------------------------
# # Division by Zero (Schema Validation)
# # ---------------------------------------------------------

# def test_division_by_zero_schema():
#     """Division by zero should raise ValidationError before DB insert."""
#     with pytest.raises(ValidationError):
#         CalculationCreate(type="division", inputs=[10, 0], user_id=uuid4())


# # ---------------------------------------------------------
# # Disallowed Operands (Model-level error)
# # ---------------------------------------------------------

# def test_disallowed_operands_in_db(db_session: Session):
#     """
#     Disallowed operands (empty list) should fail at model level.
#     SQLAlchemy will attempt to commit invalid data.
#     """
#     calc = Division(user_id=uuid4(), inputs=[])

#     db_session.add(calc)

#     with pytest.raises(Exception):
#         db_session.commit()
