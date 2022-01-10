from flask import Flask, render_template,  request, redirect, url_for, flash
from Forms import CreateUserForm, CreateCustomerForm, CreateSellerForm
import shelve, Customer, Apply
import imghdr
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from uuid import uuid4

@property
def password(self):
    raise AttributeError('Password not in readable format')

@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)

def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

app = Flask(__name__)
app.secret_key = uuid4().hex
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def home():
    return render_template('Homepage.html')

@app.route('/homepage')
def homepage():
    customers_dict = {}
    db = shelve.open('user.db', 'r')
    customers_dict = db['Users']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
    return render_template('Homepageid.html', user=current_user, customers_list=customers_list)

@app.route('/seller')
def seller():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('seller.html', user=current_user, files=files)

@app.route('/staff')
def staff():
    return render_template('staff.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        for key, value in users_dict.items():
            if value.get_email()==create_user_form.email.data and value.get_password()==create_user_form.password.data:
                #login_user(value)
                return redirect(url_for('homepage'))
            elif value.get_email()!=create_user_form.email.data:
                error='Email does not exist.'
            else:
                error='Incorrect password, try again.'
        db.close()
    return render_template('Login.html', form=create_user_form, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register',  methods=['GET', 'POST'])
def register():
    error = None
    no_of_error=0
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            customers_dict = db['Users']
        except:
            print("Error in retrieving Customers from user.db.")

        for x in customers_dict:
            if create_customer_form.email.data==customers_dict[x].get_email():
                no_of_error+=1
                error='Email been used before'
                break
            elif create_customer_form.password.data != create_customer_form.confirm.data:
                no_of_error+=1
                error='Password is must be matched'
                break
            
        if no_of_error==0:
            customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.password.data, create_customer_form.email.data, 
                                     create_customer_form.birthdate.data,
                                     create_customer_form.address.data, create_customer_form.postal.data, create_customer_form.city.data)
            customers_dict[customer.get_user_id()] = customer
            db['Users'] = customers_dict

        db.close()

        return redirect(url_for('homepage'))
    return render_template('Signup.html', form=create_customer_form, error=error)

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/sellerapplication',  methods=['GET', 'POST'])
def sellerapplication():
    create_seller_form = CreateSellerForm(request.form)
    if request.method == 'POST' and create_seller_form.validate():
        applications_dict = {}
        db = shelve.open('application.db', 'c')

        try:
            applications_dict = db['Applications']
        except:
            print("Error in retrieving Customers from Application.db.")

        application = Apply.Apply(create_seller_form.email.data, create_seller_form.password.data, create_seller_form.address.data,
                                     create_seller_form.address2.data, create_seller_form.city.data, create_seller_form.zip.data)
        applications_dict[application.get_user_id()] = application
        db['Applications'] = applications_dict

        db.close()
        
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Your application have been submitted. \nAn email will be sent you on the approval status of your application.')
        return redirect(url_for('home'))
    return render_template('sellerapplication.html', form=create_seller_form)

@app.route('/apply')
def sellerapply():
    return render_template('sellerapplication.html')

@app.route('/accountdetails')
def accountdetails():
    return render_template('accountdetails.html', user=current_user)

@app.route('/termsandconditions')
def termsandconditions():
    return render_template('termsandconditions.html')


if __name__ == '__main__':
    app.run()
