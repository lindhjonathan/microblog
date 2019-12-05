"""
Contains tests for app.main.forms.EditProfileForm class
"""
# pylint: disable=unused-argument
from unittest import mock
from wtforms.validators import ValidationError
import pytest
from app.main.forms import EditProfileForm



@mock.patch("app.main.forms.User")
def test_validate_username(mock_user, test_app):
    """
    Validate username
    """
    first = mock.Mock()
    mock_user.query.filter_by.return_value = first
    first.first.return_value = None
    username = mock.Mock()
    username.data = "john"
    assert EditProfileForm(username.data).validate_username(username) is None
    assert EditProfileForm("susan").validate_username(username) is None



@mock.patch("app.main.forms.User")
def test_validate_username_raise_exception(mock_user, test_app):
    """
    Test raise exception when username already exist
    """
    first = mock.Mock()
    mock_user.query.filter_by.return_value = first
    first.first.return_value = "john"
    username = mock.Mock()
    username.data = "john"
    with pytest.raises(ValidationError):
        EditProfileForm("susan").validate_username(username)
