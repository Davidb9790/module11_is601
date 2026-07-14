# app/models/user.py
# Line 79
from app.models.user import User

def test_user_repr():
    user = User(username="david", email="david@example.com")
    text = repr(user)
    assert "User" in text
    assert "david" in text
    assert "david@example.com" in text
