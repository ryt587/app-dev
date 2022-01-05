from wtforms import Form, StringField, SelectField, TextAreaField, validators, PasswordField
from wtforms.fields import EmailField, DateField

class CreateUserForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    
class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    postal = StringField('Postal Code', [validators.NumberRange(min=100000, max=999999), validators.DataRequired()])
    city = StringField('City', [validators.Length(max=200), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
