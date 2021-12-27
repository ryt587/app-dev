from wtforms import Form, StringField, SelectField, TextAreaField, validators, PasswordField
from wtforms.fields import EmailField, DateField

class CreateUserForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
