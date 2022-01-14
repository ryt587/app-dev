from wtforms import Form, StringField, SelectField, TextAreaField, validators, PasswordField, IntegerField, FileField
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
        validators.DataRequired()
    ], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Confirm Password"})
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    postal = IntegerField('Postal Code', [validators.NumberRange(min=100000, max=999999), validators.DataRequired()], render_kw={"placeholder": "Postal"})
    city = StringField('City', [validators.Length(max=200), validators.DataRequired()], render_kw={"placeholder": "City"})
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    address = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()], render_kw={"placeholder": "Address"})
    
class CreateSellerForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('New Password', [
        validators.DataRequired()
    ], render_kw={"placeholder": "Password"})
    address = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()],render_kw={"placeholder": "1234 Main St"})
    address2 = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()], render_kw={"placeholder": "Apartment, studio, or floor"})
    city = StringField('City', [validators.Length(max=200), validators.DataRequired()])
    postal = IntegerField('Postal Code', [validators.NumberRange(min=100000, max=999999), validators.DataRequired()])
     
class UpdateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Last Name"})
    postal = IntegerField('Postal Code', [validators.NumberRange(min=100000, max=999999), validators.DataRequired()], render_kw={"placeholder": "Postal"})
    city = StringField('City', [validators.Length(max=200), validators.DataRequired()], render_kw={"placeholder": "City"})
    address = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()], render_kw={"placeholder": "Address"})


class CreateStaffForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "Last Name"})
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('New Password', [
        validators.DataRequired()
    ], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Confirm Password"})
    role = SelectField('Staff Role', render_kw={"placeholder": "Admin"})
    phone = IntegerField('Phone Number', render_kw={"placeholder": "12345678"})
