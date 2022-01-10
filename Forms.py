from wtforms import Form, StringField, SelectField, TextAreaField, validators, PasswordField, IntegerField
from wtforms.fields import EmailField, DateField

class CreateUserForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('New Password', [
        validators.DataRequired()
    ], render_kw={"placeholder": "Password"})
    
class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Last Name"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Confirm Password"})
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    postal = IntegerField('Postal Code', [validators.NumberRange(min=100000, max=999999), validators.DataRequired()], render_kw={"placeholder": "Postal"})
    city = StringField('City', [validators.Length(max=200), validators.DataRequired()], render_kw={"placeholder": "City"})
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    address = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()], render_kw={"placeholder": "Address"})
    
class CreateSellerForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired()
    ])
    address = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    address2 = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    city = StringField('City', [validators.Length(max=200), validators.DataRequired()])
    postal = IntegerField('Postal Code', [validators.NumberRange(min=100000, max=999999), validators.DataRequired()])