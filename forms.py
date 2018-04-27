import os
from flask import session
from wtforms import (
    Form, StringField, PasswordField, validators,
    TextAreaField, FieldList, FormField, ValidationError
)


class RegistrationForm(Form):
    class Meta:
        csrf = True
        csrf_secret = os.urandom(16)

        @property
        def csrf_context(self):
            return session

    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.DataRequired(),
                                          validators.Email()])
    password = PasswordField('New Password', [
        validators.Length(min=8, max=25),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    def validate_password(form, field):
        password = field.data
        if not all([any(c.islower() for c in password),
                    any(c.isdigit() for c in password),
                    any(c.isupper() for c in password)]):
            raise ValidationError('Password should have at least 1 '
                                  'uppercase, 1 lowercase and 1 digit')


class ReferenceForm(Form):
    Text = StringField('Reference Title')
    Link = StringField('Reference Link')


class ItemInfoForm(Form):
    class Meta:
        csrf = True
        csrf_secret = os.urandom(16)

        @property
        def csrf_context(self):
            return session

    name = StringField('Name', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    categories = FieldList(StringField('Category',
                                       [validators.DataRequired()]),
                           min_entries=1)
    references = FieldList(FormField(ReferenceForm), [validators.Optional()],
                           min_entries=1)
