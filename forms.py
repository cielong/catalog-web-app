import os
from flask import session
from wtforms import (
    Form, BooleanField, StringField, PasswordField, validators,
    TextAreaField, FieldList, FormField
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
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


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
