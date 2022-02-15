from wtforms import Form, StringField, SelectField, TextAreaField, validators, PasswordField, IntegerField, ValidationError
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
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Store Name"})
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
    role = SelectField('Staff Role', render_kw={"placeholder": "Admin"},choices=[('A', 'Admin'), ('D', 'Delivery')], default='')
    phone = IntegerField('Phone Number', render_kw={"placeholder": "12345678"})

class UpdatestaffForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "Last Name"})
    role = SelectField('Staff Role', render_kw={"placeholder": "Admin"}, choices=[('', 'Select'), ('A', 'Admin'), ('D', 'Delivery')], default='')
    phone = IntegerField('Phone Number', render_kw={"placeholder": "12345678"})

class CreateElectronicForm(Form):
    Product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": "Product Name"})
    Electronics_gpu = StringField('Gpu', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "gtx 3060"})
    Electronics_cpu = StringField('Cpu', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "intel i7"})
    Electronics_storage = StringField('Storage', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "1tb"})
    Electronics_memory = StringField('Memory', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "16gb"})
    Electronics_size = StringField('Size', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "17 inches"})
    Price = IntegerField('Price', [validators.NumberRange(min=0),validators.DataRequired()], render_kw={"placeholder": "1000"})
    Product_stock = IntegerField('Product_stock', [validators.NumberRange(min=1),validators.DataRequired()], render_kw={"placeholder": "1000"})

class CreateClothingForm(Form):
    Product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": "Product Name"})
    Clothing_size = StringField('Clothing_size', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "large"})
    Clothing_colour = StringField('Clothing_colour', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "red"})
    Price = IntegerField('Price', [validators.NumberRange(min=0),validators.DataRequired()], render_kw={"placeholder": "1000"})
    Product_stock = IntegerField('Product_stock', [validators.NumberRange(min=1),validators.DataRequired()], render_kw={"placeholder": "1000"})

class CreateAccessoriesForm(Form):
    Accessory_type = SelectField('Product Type', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": ""}, choices=[('', 'Select'), ('General', 'General'), ('Sports', 'Sports')], default='')
    Product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": "Product Name"})
    Accessory_size = StringField('Accessory_size', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "large"})
    Accessory_colour = StringField('Accessory_colour', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "red"})
    Price = IntegerField('Price', [validators.NumberRange(min=0),validators.DataRequired()], render_kw={"placeholder": "1000"})
    Product_stock = IntegerField('Product_stock', [validators.NumberRange(min=1),validators.DataRequired()], render_kw={"placeholder": "1000"})

class UpdateElectronicForm(Form):
    Product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": "Product Name"})
    Electronics_gpu = StringField('Gpu', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "gtx 3060"})
    Electronics_cpu = StringField('Cpu', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "intel i7"})
    Electronics_storage = StringField('Storage', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "1tb"})
    Electronics_memory = StringField('Memory', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "16gb"})
    Electronics_size = StringField('Size', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "17 inches"})
    Price = IntegerField('Price', [validators.NumberRange(min=0),validators.DataRequired()], render_kw={"placeholder": "1000"})
    Product_stock = IntegerField('Product_stock', [validators.NumberRange(min=1), validators.NumberRange(min=0), validators.DataRequired()], render_kw={"placeholder": "1000"})


class UpdateClothingForm(Form):
    Product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": "Product Name"})
    Clothing_size = StringField('Clothing_size', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "large"})
    Clothing_colour = StringField('Clothing_colour', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "red"})
    Price = IntegerField('Price', [validators.NumberRange(min=0),validators.DataRequired()], render_kw={"placeholder": "1000"})
    Product_stock = IntegerField('Product_stock', [validators.NumberRange(min=1), validators.DataRequired()], render_kw={"placeholder": "1000"})

class UpdateAccessoriesForm(Form):
    Accessory_type = SelectField('Product Type', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": ""}, choices=[('', 'Select'), ('General', 'General'), ('Sports', 'Sports')], default='')
    Product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                               render_kw={"placeholder": "Product Name"})
    Accessory_size = StringField('Clothing_size', [validators.Length(min=1, max=150), validators.DataRequired()],
                                render_kw={"placeholder": "large"})
    Accessory_colour = StringField('Clothing_colour', [validators.Length(min=1, max=150), validators.DataRequired()],
                                  render_kw={"placeholder": "red"})
    Price = IntegerField('Price', [validators.NumberRange(min=0),validators.DataRequired()],
                         render_kw={"placeholder": "1000"})
    Product_stock = IntegerField('Product_stock', [validators.NumberRange(min=11), validators.DataRequired()], render_kw={"placeholder": "1000"})
    
class UpdateSellerForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Store Name"})
    address = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()],render_kw={"placeholder": "1234 Main St"})
    address2 = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()], render_kw={"placeholder": "Apartment, studio, or floor"})
    city = StringField('City', [validators.Length(max=200), validators.DataRequired()])
    postal = IntegerField('Postal Code', [validators.NumberRange(min=100000, max=999999), validators.DataRequired()])
    
class ForgotPsForm(Form):
    otp = StringField('OTP', [validators.DataRequired()], render_kw={"placeholder": "OTP"})
    
class ChangePsForm(Form):
    password = PasswordField('New Password', [
        validators.DataRequired()
    ], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Confirm Password"})
    
class ForgotPsEmailForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    
class OrderNumberForm(Form):
    orderno = StringField('Order Number', [validators.DataRequired()], render_kw={"placeholder": "Order Number"})

class PaymentForm(Form):
    creditcard = IntegerField('Credit Card Number', [validators.DataRequired()], render_kw={"placeholder": "Credit card Number"})
    first_name = StringField('Name', [validators.DataRequired()], render_kw={"placeholder": "Name"})
    
