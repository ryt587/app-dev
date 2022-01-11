from flask import Flask, render_template,  request, redirect, url_for, flash
from Forms import CreateUserForm, CreateCustomerForm, CreateSellerForm
import shelve, Customer, Apply
import imghdr
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from uuid import uuid4

app = Flask(__name__)
app.config['SECRET_KEY']=uuid4().hex
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

global user
user=0

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def home():
    return render_template('Homepage.html', user=user)

@app.route('/seller')
def seller():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('seller.html', files=files)

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'r')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        for key, value in users_dict.items():
            if value.get_email()==create_user_form.email.data and check_password_hash(value.get_password(), create_user_form.password.data):
                global user
                user=value
                return redirect(url_for('home'))
            elif value.get_email()!=create_user_form.email.data:
                error='Email does not exist.'
            else:
                error='Incorrect password, try again.'
        db.close()
    return render_template('Login.html', form=create_user_form, error=error)

@app.route('/logout')
def logout():
    global user
    user=0
    return redirect(url_for('home'))

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
                error='Password must be matched'
                break
            
        if no_of_error==0:
            customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data, generate_password_hash(create_customer_form.password.data, method='sha256')
                                     , create_customer_form.email.data, 
                                     create_customer_form.birthdate.data,
                                     create_customer_form.address.data, create_customer_form.postal.data, create_customer_form.city.data)
            customers_dict[customer.get_user_id()] = customer
            db['Users'] = customers_dict
            db.close()
            global user
            user=customer
            return redirect(url_for('home'))

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

@app.route('/accountdetails')
def accountdetails():
    return render_template('accountdetails.html', user=user)

@app.route('/termsandconditions')
def termsandconditions():
    return render_template('termsandconditions.html')

@app.route('/deleteUser', methods=['GET', 'POST'])
def delete_user():
    global user
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(user.get_user_id())

    db['Users'] = users_dict
    db.close()
    
    user=0
    
    return redirect(url_for('home'))

@app.route('/updateUser', methods=['GET', 'POST'])
def update_customer():
    update_customer_form = CreateCustomerForm(request.form)
    global user
    customer=user
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('user.db', 'w')
        customers_dict = db['Users']

        user.set_first_name(update_customer_form.first_name.data)
        user.set_last_name(update_customer_form.last_name.data)
        user.set_password(update_customer_form.password.data)
        user.set_email(update_customer_form.email.data)
        user.set_birthdate(update_customer_form.birthdate.data)
        user.set_address(update_customer_form.address.data)
        user.set_postal(update_customer_form.postal.data)
        user.set_city(update_customer_form.city.data)

        customers_dict[user.get_user_id()]=user
        db['Users'] = customers_dict
        db.close()

        return redirect(url_for('accountdetails'))
    else:
        customers_dict = {}
        db = shelve.open('user.db', 'r')
        customers_dict = db['Users']
        db.close()

        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.password.data = customer.get_password()
        update_customer_form.email.data=customer.get_email()
        update_customer_form.birthdate.data=customer.get_birthdate()
        update_customer_form.address.data=customer.get_address()
        update_customer_form.postal.data = customer.get_postal()
        update_customer_form.city.data = customer.get_city()

        return render_template('updateUser.html', form=update_customer_form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html'), 404


if __name__ == '__main__':
    app.run()
