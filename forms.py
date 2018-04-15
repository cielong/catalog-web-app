from wtforms import (
    Form, BooleanField, StringField, PasswordField, validators,
    TextAreaField, FieldList
)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.DataRequired(),
                                          validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class ItemInfoForm(Form):
    name = StringField('Name')
    description = TextAreaField('Description')
    categories = FieldList(StringField('Category'))
    reference = FieldList(StringField('Reference'), [validators.Optional])
