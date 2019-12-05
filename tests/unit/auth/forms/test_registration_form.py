"""
Contains tests fortest_app.auth.forms.RegistrationForm class
"""
# pylint: disable=unused-argument
from unittest import mock
from wtforms.validators import ValidationError
import pytest
from app.auth.forms import RegistrationForm



@mock.patch("app.auth.forms.User")
def test_validate_username(mock_user, test_app):
    """
    Validate username
    """
    first = mock.Mock()
    mock_user.query.filter_by.return_value = first
    first.first.return_value = None
    username = mock.Mock()
    username.data = "john"
    assert RegistrationForm().validate_username(username) is None



@mock.patch("app.auth.forms.User")
def test_validate_username_raise_exception(mock_user, test_app):
    """
    Exception is raised when username already exist.
    """
    first = mock.Mock()
    mock_user.query.filter_by.return_value = first
    first.first.return_value = "john"
    username = mock.Mock()
    username.data = "john"
    with pytest.raises(ValidationError):
        RegistrationForm().validate_username(username)



@mock.patch("app.auth.forms.User")
def test_validate_email(mock_user, test_app):
    """
    Validate email
    """
    first = mock.Mock()
    mock_user.query.filter_by.return_value = first
    first.first.return_value = None
    email = mock.Mock()
    email.data = "john@gmail.com"
    assert RegistrationForm().validate_email(email) is None



@mock.patch("app.auth.forms.User")
def test_validate_email_raise_exception(mock_user, test_app):
    """
    Exception is rased when email already exist.
    """
    first = mock.Mock()
    mock_user.query.filter_by.return_value = first
    first.first.return_value = "john@gmail.com"
    email = mock.Mock()
    email.data = "john@gmail.com"
    with pytest.raises(ValidationError):
        RegistrationForm().validate_email(email)
