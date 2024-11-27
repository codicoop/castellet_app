from django.test import TestCase

from apps.users.forms import (
    AuthenticationForm,
    EmailVerificationCodeForm,
    PasswordResetForm,
)
from apps.users.models import User


class AuthenticationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="test_name",
            surnames="test_surnames",
            email="test@test.com",
            password="test_password",
            dni="12345678A",
        )
        self.form = AuthenticationForm(
            data={
                "email": self.user.email,
                "password": self.user.password,
                "remember_me": False,
            }
        )

    def test_form(self):
        self.assertFalse(self.form.is_valid())
        self.assertEqual(
            self.form.data,
            {
                "email": self.user.email,
                "password": self.user.password,
                "remember_me": False,
            },
        )


class PasswordResetFormTest(TestCase):
    def test_form(self):
        self.form = PasswordResetForm(
            data={
                "email": "test@test.com",
            }
        )
        self.assertTrue(self.form.is_valid())
        self.assertEqual(
            self.form.data,
            {
                "email": "test@test.com",
            },
        )


class EmailVerificationCodeFormTest(TestCase):
    def test_form(self):
        self.form = EmailVerificationCodeForm(
            data={
                "email_verification_code": "1234",
            }
        )
        self.assertTrue(self.form.is_valid())
        self.assertEqual(
            self.form.data,
            {
                "email_verification_code": "1234",
            },
        )
