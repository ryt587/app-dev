from flask import Flask, render_template,  request, redirect, url_for, flash
from Forms import CreateUserForm, CreateCustomerForm
import shelve, User, Customer
import imghdr
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user

app = Flask(__name__)
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
    return render_template('Homepageid.html', user=current_user)

@app.route('/seller')
def seller():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('seller.html', user=current_user, files=files)

@app.route('/staff')
def staff():
    return render_template('staff.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        for key, value in users_dict.items():
            if value.get_email()==create_user_form.email.data and value.get_password()==create_user_form.email.data:
                login_user(value)
                return redirect(url_for('homepage'))
            elif value.get_email()!=create_user_form.email.data:
                flash('Email does not exist.')
            else:
                flash('Incorrect password, try again.')
        db.close()
        
    return render_template('login.html', form=create_user_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register',  methods=['GET', 'POST'])
def register():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.password.data, create_customer_form.email.data, 
                                     create_customer_form.birthdate.data,
                                     create_customer_form.address.data, create_customer_form.postal.data, create_customer_form.city.data)
        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict

        db.close()

        return redirect(url_for('login'))
    return render_template('Resgistration.html', form=create_customer_form)

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

'''
@app.route('/sellerapplication',  methods=['GET', 'POST'])
def sellerapplication():
    create_seller_form = CreateSellerForm(request.form)
    if request.method == 'POST' and create_seller_form.validate():
        applications_dict = {}
        db = shelve.open('application.db', 'c')

        try:
            customers_dict = db['Applications']
        except:
            print("Error in retrieving Customers from Application.db.")

        application = Customer.Customer(create_seller_form.first_name.data, create_seller_form.last_name.data,
                                     create_seller_form.password.data, create_seller_form.email.data, 
                                     create_seller_form.birthdate.data,
                                     create_seller_form.address.data, create_seller_form.postal.data, create_seller_form.city.data)
        customers_dict[customer.get_customer_id()] = application
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
'''

@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)


@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_password()

        return render_template('updateUser.html', form=update_user_form)
    
@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_gender(update_customer_form.password.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_address(update_customer_form.address.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.password.data = customer.get_password()
        update_customer_form.email.data=customer.get_email()
        update_customer_form.date_joined.data=customer.get_date_joined()
        update_customer_form.address.data=customer.get_address()

        return render_template('updateCustomer.html', form=update_customer_form)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))

@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']

    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('retrieve_customers'))

@app.route('/apply')
def sellerapply():
    return render_template('sellerapplication.html')

@app.route('/accountdetails')
def accountdetails():
    return render_template('accountdetails.html')

@app.route('/termsandconditions')
def termsandconditions():
    return render_template('termsandconditions.html')


if __name__ == '__main__':
    app.run()
