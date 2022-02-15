from flask import Flask, render_template,  request, redirect, url_for, abort
import Forms as f
import shelve, Customer, Apply, Staff, Seller, Electronics, Clothing, Transaction, Accessories, Refund
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from uuid import uuid4
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from flask_mail import Mail, Message
import datetime as d
import itertools
import pyotp
import json

app = Flask(__name__)
app.config['SECRET_KEY']=uuid4().hex
app.config['UPLOAD_PATH'] = 'static/images/cert/'
app.config['UPLOAD_FOLDER'] = 'static/images/product_image/'
app.config["ALLOWED_IMAGE_EXTENSIONS"]=['png', 'jpg', 'jfif']
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_PORT"] = 465
app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_USERNAME'] = 'chuaandspencer@gmail.com'
app.config['MAIL_PASSWORD'] = 'nypappdev2022'
app.config['MAIL_DEFAULT_SENDER'] = 'chuaandspencer@gmail.com'

mail=Mail(app)

db = shelve.open('user.db', 'c')
earnings_dict={}
try:
    if 'Earnings' in db:
        earnings_dict=db['Earnings']
    else:
        db['Earnings']=earnings_dict
    for x in range(30,-1,-1):
        if not (d.date.today() - d.timedelta(x) in earnings_dict):
            earnings_dict[d.date.today() - d.timedelta(x)]=0
    db['Earnings']=earnings_dict
except:
    print("Error in retrieving earnings from user.db.")
db.close()
db = shelve.open('user.db', 'c')
sellers_dict={}
try:
    if 'Users' in db:
        sellers_dict=db['Users']
    else:
        db['Users']=sellers_dict
    for x in sellers_dict:
        if isinstance(sellers_dict[x],Seller.Seller):
            for y in range(30,-1,-1):
                if not (d.date.today() - d.timedelta(y) in sellers_dict[x].get_earned()):
                    earned=sellers_dict[x].get_earned()
                    earned[d.date.today()- d.timedelta(y)]=0
                    sellers_dict[x].set_earned(earned)
    db['Users']=sellers_dict
except:
    print("Error in retrieving seller from user.db.")
db.close()

global user
user=0

def allowed_image(filename):

    if not ("." in filename):
        return False

    ext = filename.rsplit(".")[-1]

    if ext.lower() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False
    
def get_graph(title,earning_dict):
    earning_dict=dict(reversed(list(earning_dict.items())))
    earning_dict=dict(itertools.islice(earning_dict.items(), 30))
    earning_dict=dict(reversed(list(earning_dict.items())))
    plt.figure(figsize=(10, 6.5))
    plt.title(title)
    plt.plot([x.strftime("%Y/%m/%d") for x in earning_dict],[x for x in earning_dict.values()])
    plt.ylim(ymin=0)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Revenue earned")
    # Save it to a temporary buffer.
    output = BytesIO()
    plt.savefig(output, format='png')
    output.seek(0)
    # Embed the result in the html output.
    data=base64.b64encode(output.getvalue())
    return data


@app.route('/')
def home():
    return render_template('Homepage.html', user=user)


@app.route('/seller')
def seller():
    return render_template('seller.html', user=user)


@app.route('/staff')
def staff():
    return render_template('staff.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    create_user_form = f.CreateUserForm(request.form)
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
                if isinstance(value, Customer.Customer):
                    return redirect(url_for('home'))
                elif isinstance(value, Seller.Seller):
                    return redirect(url_for('seller'))
                elif isinstance(value, Staff.Staff):
                    return redirect(url_for('staff'))
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
    create_customer_form = f.CreateCustomerForm(request.form)
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
    create_seller_form = f.CreateSellerForm(request.form)
    error=None
    no_of_error=0
    if request.method == 'POST' and create_seller_form.validate():
        file = request.files['file']
        applications_dict = {}
        users_dict ={}
        with shelve.open('user.db', 'c') as db:
            try:
                if 'Applications' in db:
                    applications_dict = db['Applications']
                else:
                    db['Applications'] = applications_dict
            except:
                print("Error in retrieving Customers from application.db.")
            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db['Users'] = users_dict
            except:
                print("Error in retrieving Customers from User.db.")
            if not allowed_image(file.filename):
                    error="Missing image or invalid format of image"
                    no_of_error+=1
            elif applications_dict!={}:
                for x in applications_dict:
                    if  create_seller_form.email.data==applications_dict[x].get_email():
                        error="Email has been used before"
                        no_of_error+=1
                        break
            elif users_dict!={}:
                for x in users_dict:
                    if  create_seller_form.email.data==users_dict[x].get_email():
                        error="Email has been used before"
                        no_of_error+=1
                        break
            if no_of_error==0:
                application = Apply.Apply(create_seller_form.name.data, create_seller_form.email.data, create_seller_form.password.data, create_seller_form.address.data,
                                        create_seller_form.address2.data, create_seller_form.city.data, create_seller_form.postal.data, file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(file.filename)))
                file_type='.'+file.filename.split('.')[-1]
                os.rename(app.config['UPLOAD_PATH'] + secure_filename(file.filename), app.config['UPLOAD_PATH']+(str(application.get_apply_id())+file_type))
                application.set_image(str(application.get_apply_id())+file_type)
                applications_dict[application.get_apply_id()] = application
                db['Applications'] = applications_dict
                return redirect(url_for('waiting'))
    return render_template('sellerapplication.html', form=create_seller_form, error=error, user=user)


@app.route('/accountdetails')
def accountdetails():
    return render_template('accountdetails.html', user=user)


@app.route('/termsandconditions')
def termsandconditions():
    return render_template('termsandconditions.html')

@app.route('/Aboutus')
def Aboutus():
    return render_template('AboutUs.html')


@app.route('/deleteUser/', methods=['GET', 'POST'])
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


@app.route('/updateUser/', methods=['GET', 'POST'])
def update_customer():
    update_customer_form = f.UpdateCustomerForm(request.form)
    global user
    customer=user
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('user.db', 'w')
        customers_dict = db['Users']

        user.set_name(update_customer_form.first_name.data)
        user.set_last_name(update_customer_form.last_name.data)
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

        update_customer_form.first_name.data = customer.get_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.address.data=customer.get_address()
        update_customer_form.postal.data = customer.get_postal()
        update_customer_form.city.data = customer.get_city()

        return render_template('updateUser.html', form=update_customer_form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html'), 404


@app.route('/viewapply')
def viewapply():
    applications_dict={}
    with shelve.open('user.db', 'c') as db:
        try:
            applications_dict = db['Applications']
        except:
            print("Error in retrieving Customers from application.db.")
        applications_list=[]
        if applications_dict!={}:
            for x in applications_dict:
                applications_list.append(applications_dict[x])
    while len(applications_list) < 5:
        applications_list.append(0)
    return render_template('viewapplication.html', applications_list=applications_list, user=user)


@app.route('/retrieveapply/<int:id>', methods=['GET', 'POST'])
def retrieve(id):
    with shelve.open('user.db', 'c') as db:
        try:
            applications_dict = db['Applications']
        except:
            print("Error in retrieving Customers from application.db.")
        application=applications_dict[id]
    return render_template('retrieveapplication.html', application=application, user=user)


@app.route('/reject/<int:id>', methods=['GET', 'POST'])
def reject_seller(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Applications']
    applications=users_dict[id]
    msg = Message("Application rejected",
                  sender="chuaandspencer@example.com",
                  recipients=[applications.get_email()])
    msg.body="Your application to be a seller at Chua And Spencer's have been rejected"
    mail.send(msg)
    os.remove(app.config['UPLOAD_PATH']+str(applications.get_image()))
    users_dict.pop(id)

    db['Applications'] = users_dict
    db.close()

    return redirect(url_for('viewapply'))

@app.route('/createStaff',  methods=['GET', 'POST'])
def createStaff():
    create_staff_form = f.CreateStaffForm(request.form)
    error=None
    no_of_error=0
    if request.method == 'POST' and create_staff_form.validate():
        staff_dict = {}
        with shelve.open('user.db', 'c') as db:
            try:
                staff_dict = db['Users']
            except:
                print("Error in retrieving Customers from staff.db.")
            if error!=None:
                no_of_error+=1

            for x in staff_dict:
                if create_staff_form.email.data==staff_dict[x].get_email():
                    no_of_error+=1
                    error='Email been used before'
                    break
                elif create_staff_form.password.data != create_staff_form.confirm.data:
                    no_of_error+=1
                    error='Password must be matched'
                    break
            if no_of_error==0:
                staff = Staff.Staff(create_staff_form.first_name.data, create_staff_form.last_name.data, create_staff_form.email.data,
                                        generate_password_hash(create_staff_form.password.data, method='sha256'),
                                        create_staff_form.role.data, create_staff_form.phone.data)
                staff_dict[staff.get_staff_id()] = staff
                db['Users'] = staff_dict
                return redirect(url_for('staff'))
    return render_template('createStaff.html', form=create_staff_form, error=error, user=user)


@app.route('/retrievestaff')
def retrieve_staff():
    customers_dict = {}
    db = shelve.open('user.db', 'r')
    customers_dict = db['Users']
    db.close()

    customers_list = []
    for key in customers_dict:
        if str(key)[:2]=='St':
            customer = customers_dict.get(key)
            customers_list.append(customer)
    while len(customers_list) < 5:
        customers_list.append(0)
    return render_template('retrievestaff.html', users_list=customers_list, user=user)


@app.route('/updatestaff/<id>', methods=['GET', 'POST'])
def update_staff(id):
    update_staff_form = f.UpdatestaffForm(request.form)
    global user
    if request.method == 'POST' and update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('user.db', 'w')
        staff_dict = db['Users']

        staff = staff_dict[id]
        staff.set_name(update_staff_form.first_name.data)
        staff.set_last_name(update_staff_form.last_name.data)
        staff.set_staff_role(update_staff_form.role.data)
        staff.set_phone_number(update_staff_form.phone.data)

        staff_dict[user.get_staff_id()]=user
        db['Users'] = staff_dict

        db.close()

        return redirect(url_for('retrieve_staff'))
    else:
        staff_dict = {}
        db = shelve.open('user.db', 'r')
        staff_dict = db['Users']
        db.close()
        staff = staff_dict[id]
        update_staff_form.first_name.data = staff.get_name()
        update_staff_form.last_name.data = staff.get_last_name()
        update_staff_form.role.data = staff.get_staff_role()
        update_staff_form.phone.data = staff.get_phone_number()

        return render_template('updatestaff.html', form=update_staff_form, user=user)


@app.route('/deletestaff/<id>', methods=['GET', 'POST'])
def delete_staff(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_staff'))

@app.route('/accountdetailstaff')
def accountdetailstaff():
    return render_template('accountdetailstaff.html', user=user)

@app.route('/createproduct', methods=['GET', 'POST'])
def CreateProduct():
    category=request.form.get('category')
    if category=="electronic":
        return redirect(url_for('create_electronic'))
    elif category=="clothing":
        return redirect(url_for('create_clothing'))
    elif category=="accessories":
        return redirect(url_for('create_accessory'))
    return render_template('products.html', user=user)

@app.route('/createproduct/electronic',  methods=['GET', 'POST'])
def create_electronic():
    create_product_form = f.CreateElectronicForm(request.form)
    error=None
    no_of_error=0
    if request.method == 'POST' and create_product_form.validate():
        file = request.files['file']
        product_dict = {}
        with shelve.open('user.db', 'c') as db:
            try:
                product_dict = db['Products']
            except:
                print("Error in retrieving Customers from Product.db.")
            if not allowed_image(file.filename):
                    error="Missing image or invalid format of image"
                    no_of_error+=1
            if no_of_error==0:
                Product = Electronics.Electronics(create_product_form.Product_name.data, create_product_form.Product_stock.data, secure_filename(file.filename), user.get_seller_id(),create_product_form.Price.data,
                                                  create_product_form.Electronics_gpu.data, create_product_form.Electronics_cpu.data,
                                                  create_product_form.Electronics_storage.data, create_product_form.Electronics_memory.data,
                                                  create_product_form.Electronics_size.data)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                file_type='.'+file.filename.split('.')[-1]
                os.rename(app.config['UPLOAD_FOLDER'] + secure_filename(file.filename), app.config['UPLOAD_FOLDER']+(str(Product.get_product_id())+file_type))
                Product.set_product_image(str(Product.get_product_id())+file_type)
                product_dict[Product.get_product_id()] = Product
                db['Products'] = product_dict
                return redirect(url_for('seller'))
    return render_template('electronic_products.html', form=create_product_form, error=error, user=user)

@app.route('/createproduct/accessories',  methods=['GET', 'POST'])
def create_accessory():
    create_accessory_form = f.CreateAccessoriesForm(request.form)
    error=None
    no_of_error=0
    if request.method == 'POST' and create_accessory_form.validate():
        file = request.files['file']
        product_dict = {}
        with shelve.open('user.db', 'c') as db:
            try:
                product_dict = db['Products']
            except:
                print("Error in retrieving Customers from Product.db.")
            if not allowed_image(file.filename):
                    error="Missing image or invalid format of image"
                    no_of_error+=1
            if no_of_error==0:
                Product = Accessories.Accessories(create_accessory_form.Product_name.data, create_accessory_form.Product_stock.data, secure_filename(file.filename), user.get_seller_id(),create_accessory_form.Price.data,
                                            create_accessory_form.Accessory_colour.data,create_accessory_form.Accessory_size.data,create_accessory_form.Accessory_type.data)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                file_type='.'+file.filename.split('.')[-1]
                os.rename(app.config['UPLOAD_FOLDER'] + secure_filename(file.filename), app.config['UPLOAD_FOLDER']+(str(Product.get_product_id())+file_type))
                Product.set_product_image(str(Product.get_product_id())+file_type)
                product_dict[Product.get_product_id()] = Product
                db['Products'] = product_dict
                return redirect(url_for('seller'))
    return render_template('accessory_products.html', form=create_accessory_form, error=error, user=user)

@app.route('/createproduct/clothing',  methods=['GET', 'POST'])
def create_clothing():
    create_product_form = f.CreateClothingForm(request.form)
    error=None
    no_of_error=0
    if request.method == 'POST' and create_product_form.validate():
        file = request.files['file']
        product_dict = {}
        with shelve.open('user.db', 'c') as db:
            try:
                product_dict = db['Products']
            except:
                print("Error in retrieving Customers from Product.db.")
            if not allowed_image(file.filename):
                    error="Missing image or invalid format of image"
                    no_of_error+=1
            if no_of_error==0:
                Product = Clothing.Clothing(create_product_form.Product_name.data, create_product_form.Product_stock.data, secure_filename(file.filename), user.get_seller_id(),create_product_form.Price.data,
                                            create_product_form.Clothing_colour.data, create_product_form.Clothing_size.data)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                file_type='.'+file.filename.split('.')[-1]
                os.rename(app.config['UPLOAD_FOLDER'] + secure_filename(file.filename), app.config['UPLOAD_FOLDER']+(str(Product.get_product_id())+file_type))
                Product.set_product_image(str(Product.get_product_id())+file_type)
                product_dict[Product.get_product_id()] = Product
                db['Products'] = product_dict
                return redirect(url_for('seller'))
    return render_template('clothing_products.html', form=create_product_form, error=error, user=user)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product_dict = {}
    db = shelve.open('user.db', 'w')
    product_dict = db['Products']
    product=product_dict[id]
    if isinstance(product, Electronics.Electronics):
        return redirect(url_for('update_electronic',id=id))
    elif isinstance(product, Clothing.Clothing):
        return redirect(url_for('update_clothing',id=id))
    elif isinstance(product, Accessories.Accessories):
        return redirect(url_for('update_accessories',id=id))
    
@app.route('/updateproduct/electronic/<int:id>', methods=['GET', 'POST'])
def update_electronic(id):
    update_product_form = f.UpdateElectronicForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        product_dict = {}
        db = shelve.open('user.db', 'w')
        product_dict = db['Products']

        product = product_dict[id]
        product.set_name(update_product_form.Product_name.data)
        product.set_product_stock(update_product_form.Product_stock.data)
        product.set_price(update_product_form.Price.data)
        product.set_gpu(update_product_form.Electronics_gpu.data)
        product.set_cpu(update_product_form.Electronics_cpu.data)
        product.set_storage(update_product_form.Electronics_storage.data)
        product.set_memory(update_product_form.Electronics_memory.data)
        product.set_size(update_product_form.Electronics_size.data)

        product_dict[product.get_product_id()] = product
        db['Products'] = product_dict

        db.close()

        return redirect(url_for('productlist'))
    else:
        product_dict = {}
        db = shelve.open('user.db', 'r')
        product_dict = db['Products']
        db.close()
        product= product_dict[id]
        update_product_form.Product_name.data = product.get_name()
        update_product_form.Product_stock.data = product.get_product_stock()
        update_product_form.Price.data = product.get_price()
        update_product_form.Electronics_gpu.data = product.get_gpu()
        update_product_form.Electronics_cpu.data = product.get_cpu()
        update_product_form.Electronics_storage.data = product.get_storage()
        update_product_form.Electronics_memory.data = product.get_memory()
        update_product_form.Electronics_size.data = product.get_size()

        return render_template('updateelectronic.html', form=update_product_form, user=user)


@app.route('/updateproduct/clothing/<int:id>', methods=['GET', 'POST'])
def update_clothing(id):
    update_product_form = f.UpdateClothingForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        product_dict = {}
        db = shelve.open('user.db', 'w')
        product_dict = db['Products']

        product = product_dict[id]
        product.set_name(update_product_form.Product_name.data)
        product.set_product_stock(update_product_form.Product_stock.data)
        product.set_price(update_product_form.Price.data)
        product.set_colour(update_product_form.Clothing_colour.data)
        product.set_size(update_product_form.Clothing_size.data)

        product_dict[product.get_product_id()] = product
        db['Products'] = product_dict

        db.close()

        return redirect(url_for('productlist'))
    else:
        product_dict = {}
        db = shelve.open('user.db', 'r')
        product_dict = db['Products']
        db.close()
        product= product_dict[id]
        update_product_form.Product_name.data = product.get_name()
        update_product_form.Product_stock.data = product.get_product_stock()
        update_product_form.Price.data = product.get_price()
        update_product_form.Clothing_colour.data = product.get_colour()
        update_product_form.Clothing_size.data = product.get_size()

        return render_template('updateclothing.html', form=update_product_form, user=user)

@app.route('/updateproduct/accessories/<int:id>', methods=['GET', 'POST'])
def update_accessories(id):
    update_product_form = f.UpdateAccessoriesForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        product_dict = {}
        db = shelve.open('user.db', 'w')
        product_dict = db['Products']

        product = product_dict[id]
        product.set_accessory_type(update_product_form.Accessory_type.data)
        product.set_name(update_product_form.Product_name.data)
        product.set_product_stock(update_product_form.Product_stock.data)
        product.set_price(update_product_form.Price.data)
        product.set_colour(update_product_form.Accessory_colour.data)
        product.set_size(update_product_form.Accessory_size.data)

        product_dict[product.get_product_id()] = product
        db['Products'] = product_dict

        db.close()

        return redirect(url_for('productlist'))
    else:
        product_dict = {}
        db = shelve.open('user.db', 'r')
        product_dict = db['Products']
        db.close()
        product= product_dict[id]
        update_product_form.Product_name.data = product.get_name()
        update_product_form.Product_stock.data = product.get_product_stock()
        update_product_form.Price.data = product.get_price()
        update_product_form.Accessory_type.data = product.get_accessory_type()
        update_product_form.Accessory_colour.data = product.get_colour()
        update_product_form.Accessory_size.data = product.get_size()

        return render_template('updateaccessories.html', form=update_product_form, user=user)


@app.route('/deleteproduct/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('user.db', 'w')
    products_dict = db['Products']
    product=products_dict[id]
    product.set_product_stock(0)
    product.set_active(False)
    products_dict[id]=product
    db['Products'] = products_dict
    db.close()
    return redirect(url_for('productlist'))


@app.route('/productlist')
def productlist():
    product_dict = {}
    db = shelve.open('user.db', 'r')
    product_dict = db['Products']
    db.close()

    product_list = []
    for key in product_dict:
        product = product_dict.get(key)
        if product.get_created_product()==user.get_seller_id():
            product_list.append(product)
    return render_template('productlist.html', product_list=product_list, user=user)

@app.route('/approve/<int:id>')
def approve(id):
    application_dict = {}
    with shelve.open('user.db', 'c') as db:
        try:
            application_dict = db['Applications']
        except:
            print("Error in retrieving Customers from staff.db.")
        application=application_dict[id] 
        msg = Message("Application approved",
                  sender="chuaandspencer@example.com",
                  recipients=[application.get_email()])
        msg.body="Your application to be a seller at Chua And Spencer's is approved. To log in:\nEmail: {}\nPassword: {}".format(application.get_email(), application.get_password())
        mail.send(msg)
        os.remove(app.config['UPLOAD_PATH']+str(application.get_image()))
        application_dict.pop(id)
        db['Applications'] = application_dict
        try:
            seller_dict = db['Users']
        except:
            print("Error in retrieving Customers from staff.db.")
        seller = Seller.Seller(application.get_name(), application.get_email(), generate_password_hash(application.get_password()), application.get_address(),application.get_address2(), application.get_city(), application.get_postal())
        seller_dict[seller.get_seller_id()] = seller
        db['Users'] = seller_dict
        return redirect(url_for('viewapply'))

@app.route('/accountdetailseller')
def accountdetailseller():
    return render_template('accountdetailseller.html', user=user)

@app.route('/updateseller', methods=['GET', 'POST'])
def update_seller():
    update_seller_form = f.UpdateSellerForm(request.form)
    global user
    if request.method == 'POST' and update_seller_form.validate():
        seller_dict = {}
        db = shelve.open('user.db', 'w')
        seller_dict = db['Users']

        seller = user
        seller.set_name(update_seller_form.name.data)
        seller.set_address(update_seller_form.address.data)
        seller.set_address2(update_seller_form.address2.data)
        seller.set_city(update_seller_form.city.data)
        seller.set_postal_code(update_seller_form.postal.data)

        seller_dict[user.get_seller_id()]=seller
        db['Users'] = seller_dict

        db.close()

        return redirect(url_for('accountdetailseller'))
    else:
        seller_dict = {}
        db = shelve.open('user.db', 'r')
        seller_dict = db['Users']
        db.close()
        seller = user
        update_seller_form.name.data = seller.get_name()
        update_seller_form.address.data = seller.get_address()
        update_seller_form.address2.data = seller.get_address2()
        update_seller_form.city.data = seller.get_city()
        update_seller_form.postal.data = seller.get_postal_code()

        return render_template('updateseller.html', form=update_seller_form, user=user)
@app.route('/deleteseller', methods=['GET', 'POST'])
def delete_seller():
    global user
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']
    products_dict=db['Products']
    products_list=[]
    for x in products_dict:
        if products_dict[x].get_created_product()==user.get_seller_id():
            products_list.append(products_dict[x])
    for x in products_list:
        x.set_product_stock(0)
        x.set_created_product(0)
        products_dict[x.get_product_id()]=x

    users_dict.pop(user.get_seller_id())
    db['Products'] = products_dict
    db['Users'] = users_dict
    db.close()

    user=0

    return redirect(url_for('home'))

@app.route('/reportseller')
def reportseller():
    total_impression=0
    db = shelve.open('user.db', 'c')
    productlist=[]
    users_dict={}
    if 'Products' in db:
        users_dict=db['Products']
    else:
        db['Products']=users_dict
    if users_dict!={}:
        for x in users_dict:
            if users_dict[x].get_created_product()==user.get_seller_id():
                total_impression+=users_dict[x].get_impression()
                productlist.append(users_dict[x])
    def byimpression(product):
        return product.get_impression()
    productlist=sorted(productlist, key= byimpression)
    db.close()
    return render_template('reportseller.html', user=user, productlist=productlist, total_impression=total_impression)

@app.route('/reportstaff')
def reportstaff():
    db = shelve.open('user.db', 'c')
    earnings_dict={}
    try:
        if 'Earnings' in db:
            earnings_dict=db['Earnings']
    except:
        print("Error in retrieving Users from user.db.")
    db.close()
    data=get_graph("Revenue from past 30 days",earnings_dict)
    return render_template('reportstaff.html', user=user, result=data.decode('utf8'))

@app.route('/faq')
def faq():
    return render_template('faq.html', user=user)

@app.route('/waitingapplication')
def waiting():
    return render_template('waitingapplication.html', user=user)

@app.route('/graphseller')
def graphseller():
    seller_earnings_dict=user.get_earned()
    data=get_graph("Revenue from past 30 days",seller_earnings_dict)
    return render_template('graphseller.html', user=user, result=data.decode('utf8'))


@app.route('/retrievecustomers')
def retrieve_customer():
    customers_dict = {}
    db = shelve.open('user.db', 'r')
    customers_dict = db['Users']
    db.close()

    customers_list = []
    for key in customers_dict:
        if str(key)[0]=='C':
            customer = customers_dict.get(key)
            customers_list.append(customer)
    while len(customers_list) < 5:
        customers_list.append(0)
    return render_template('retrievecustomers.html', users_list=customers_list, user=user)

@app.route('/retrievesellers')
def retrieve_seller():
    customers_dict = {}
    db = shelve.open('user.db', 'r')
    customers_dict = db['Users']
    db.close()

    customers_list = []
    for key in customers_dict:
        if str(key)[:2]=='Se':
            customer = customers_dict.get(key)
            customers_list.append(customer)
    while len(customers_list) < 5:
        customers_list.append(0)
    return render_template('retrievesellers.html', users_list=customers_list, user=user)

@app.route('/banUser/<id>', methods=['GET', 'POST'])
def ban_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']
    products_dict = db['Products']
    products_list = []
    user2=users_dict[id]
    if isinstance(user2, Seller.Seller):
        for x in products_dict:
            if products_dict[x].get_created_product()==user2.get_seller_id():
                products_list.append(products_dict[x])
        for x in products_list:
            x.set_product_stock(0)
            x.set_created_product(0)
            products_dict[x.get_product_id()]=x
    msg = Message("Account have been banned",
                  sender="chuaandspencer@example.com",
                  recipients=[users_dict[id].get_email()])
    msg.body="You have been banned from using Chua and Spencer. "
    users_dict.pop(id)
    mail.send(msg)

    db['Users'] = users_dict
    db['Products'] = products_dict
    db.close()
    if 'customer' in request.referrer:
        return redirect(url_for('retrieve_customer'))
    elif 'seller' in request.referrer:
        return redirect(url_for('retrieve_seller'))

@app.route('/forgetps/<id>', methods=['GET', 'POST'])
def forgetps(id):
    error=None 
    users_dict={}
    db = shelve.open('user.db', 'c')
    try:
        if 'Users' in db:
            users_dict=db['Users']
        else:
            db['Users']=users_dict
    except:
        print("Error in retrieving Users from user.db.")
    db.close()
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=425.41)
    msg = Message("OTP to change password",
                  sender="chuaandspencer@example.com",
                  recipients=[users_dict[id].get_email()])
    msg.body="Your OTP to change password is:\n{}\nYou have 5 minutes to enter the otp, or it will be invalid".format(totp.now())
    mail.send(msg)
    forgot_ps_form = f.ForgotPsForm(request.form)
    if request.method == 'POST' and forgot_ps_form.validate():
        if totp.verify(forgot_ps_form.otp.data):
            error="Invalid OTP"
        else:
            return redirect(url_for('changeps', id=id))
    return render_template('forgotps.html',  user=user, error=error, form=forgot_ps_form)

@app.route('/changeps/<id>', methods=['GET', 'POST'])
def changeps(id):
    error=None
    change_ps_form = f.ChangePsForm(request.form)
    db = shelve.open('user.db', 'c')
    users_dict={}
    try:
        if 'Users' in db:
            users_dict=db['Users']
        else:
            db['Users']=users_dict
    except:
        print("Error in retrieving Users from user.db.")
    if request.method == 'POST' and change_ps_form.validate():
        if change_ps_form.password.data!=change_ps_form.confirm.data:
            error="Password must be matched"
        else:
            users_dict[id].set_password(generate_password_hash(change_ps_form.password.data))
            db['Users']=users_dict
            db.close()
            return redirect(url_for('login'))
    return render_template('changeps.html',  user=user, error=error, form=change_ps_form)

@app.route('/forgotpsemail', methods=['GET', 'POST'])
def forgotpsemail():
    error=None
    forgot_ps_email_form = f.ForgotPsEmailForm(request.form)
    db = shelve.open('user.db', 'c')
    users_dict={}
    try:
        if 'Users' in db:
            users_dict=db['Users']
        else:
            db['Users']=users_dict
    except:
        print("Error in retrieving Users from user.db.")
    db.close()
    if request.method == 'POST' and forgot_ps_email_form.validate():
        for x in users_dict:
            if users_dict[x].get_email()==forgot_ps_email_form.email.data:
                return redirect(url_for('forgetps', id=x))
            else:
                error="Email does not exist"
    return render_template('forgotpsemail.html',  user=user, error=error, form=forgot_ps_email_form)

@app.route('/productdetail/<int:id>')
def productdetail(id):
    db=shelve.open('user.db', 'c')
    products_dict={}
    try:
        if 'Products' in db:
            products_dict=db['Products']
        else:
            db['Products']=products_dict
    except:
        print("Error in retrieving Products from user.db.")
    sellers_dict={}
    try:
        if 'Users' in db:
            sellers_dict=db['Users']
        else:
            db['Users']=sellers_dict
    except:
        print("Error in retrieving sellers from user.db.") 
    product=products_dict[id]
    product.set_impression(product.get_impression()+1)
    products_dict[id]=product
    db['Products']=products_dict
    db.close()
    seller=sellers_dict[product.get_created_product()]
    if user!=0 and id in user.get_wishlist():
        wishlist=True
    elif user!=0 and not (id in user.get_wishlist()):
        wishlist=False
    else:
        wishlist=0
    if isinstance(product, Electronics.Electronics):
        return render_template("productdetailelectronic.html", x=product, user=user, seller=seller, wishlist=wishlist)
    elif isinstance(product, Clothing.Clothing):
        return render_template("productdetailclothing.html", x=product, user=user, seller=seller, wishlist=wishlist)
    elif isinstance(product, Accessories.Accessories):
        return render_template("productdetailaccessories.html", x=product, user=user, seller=seller, wishlist=wishlist)

@app.route('/addwishlist/<int:id>')
def addwishlist(id):
    db=shelve.open('user.db', 'c')
    users_dict={}
    try:
        if 'Users' in db:
            users_dict=db['Users']
        else:
            db['Users']=users_dict
    except:
        print("Error in retrieving Users from user.db.")
    wishlist=user.get_wishlist()
    wishlist[id]=0
    user.set_wishlist(wishlist)
    users_dict[user.get_user_id()]=user
    db['Users']=users_dict
    db.close()
    return redirect(url_for('productdetail', id=id))

@app.route('/removewishlist/<int:id>')
def removewishlist(id):
    db=shelve.open('user.db', 'c')
    users_dict={}
    try:
        if 'Users' in db:
            users_dict=db['Users']
        else:
            db['Users']=users_dict
    except:
        print("Error in retrieving Users from user.db.")
    wishlist=user.get_wishlist()
    wishlist.pop(id)
    user.set_wishlist(wishlist)
    users_dict[user.get_user_id()]=user
    db['Users']=users_dict
    db.close()
    if 'productdetail' in request.referrer:
        return redirect(url_for('productdetail', id=id))
    elif 'wishlist' in request.referrer:
        return redirect(url_for('retrievewishlist'))
    else:
        abort(404)

@app.route('/retrievewishlist')
def retrievewishlist():
    db=shelve.open('user.db', 'c')
    products_dict={}
    try:
        if 'Products' in db:
            products_dict=db['Products']
        else:
            db['Products']=products_dict
    except:
        print("Error in retrieving Products from user.db.")
    db.close()
    products_list=[int(x) for x in user.get_wishlist()]
    for i, x in enumerate(products_list):
        products_list[i]=products_dict[x]
    while len(products_list)<5:
        products_list.append(0)
    return render_template("retrievewishlist.html", user=user, product_list=products_list)

@app.route('/removecart/<int:id>')
def removecart(id):
    db=shelve.open('user.db', 'c')
    users_dict={}
    try:
        if 'Users' in db:
            users_dict=db['Users']
        else:
            db['Users']=users_dict
    except:
        print("Error in retrieving Users from user.db.")
    wishlist=user.get_cart()
    wishlist.pop(id)
    user.set_cart(wishlist)
    users_dict[user.get_user_id()]=user
    db['Users']=users_dict
    db.close()
    if 'productdetail' in request.referrer:
        return redirect(url_for('productdetail', id=id))
    elif 'cart' in request.referrer:
        return redirect(url_for('retrievecart'))
    else:
        abort(404)

@app.route('/addcart/<int:id>')
def addcart(id):
    db=shelve.open('user.db', 'c')
    users_dict={}
    try:
        if 'Users' in db:
            users_dict=db['Users']
        else:
            db['Users']=users_dict
    except:
        print("Error in retrieving Users from user.db.")
    wishlist=user.get_cart()
    wishlist[id]=0
    user.set_cart(wishlist)
    users_dict[user.get_user_id()]=user
    db['Users']=users_dict
    db.close()
    if 'productdetail' in request.referrer:
        return redirect(url_for('productdetail', id=id))
    elif 'wishlist' in request.referrer:
        return redirect(url_for('retrievewishlist'))
    else:
        abort(404)

@app.route('/retrievecart')
def retrievecart():
    db=shelve.open('user.db', 'c')
    products_dict={}
    try:
        if 'Products' in db:
            products_dict=db['Products']
        else:
            db['Products']=products_dict
    except:
        print("Error in retrieving Products from user.db.")
    db.close()
    products_list=[int(x) for x in user.get_cart()]
    for i, x in enumerate(products_list):
        products_list[i]=products_dict[x]
    while len(products_list)<5:
        products_list.append(0)
    return render_template("retrievecart.html", user=user, products_list=products_list)

@app.route('/pastorder', methods=['GET', 'POST'])
def pastorder():
    db=shelve.open('user.db', 'c')
    transactions_dict={}
    try:
        if 'Transactions' in db:
            transactions_dict=db['Transactions']
        else:
            db['Transactions']=transactions_dict
    except:
        print("Error in retrieving Transactions from user.db.")
    products_dict={}
    try:
        if 'Products' in db:
            products_dict=db['Products']
        else:
            db['Products']=products_dict
    except:
        print("Error in retrieving Transactions from user.db.")
    db.close()
    transaction_list=[]
    product_list={}
    for x in transactions_dict:
        if transactions_dict[x].get_delivered_date()!=0 and transactions_dict[x].get_product_list()!=0 and transactions_dict[x].get_product_list()!={}:
            transaction_list.append(transactions_dict[x])
    for x in transaction_list:
        if x.get_product_list()!=0:
            product_list[x]=[]
            for y in x.get_product_list():
                product_list[x].append(y)
    return render_template("pastorder.html", user=user, transaction_list=transaction_list, product_list=product_list, product_dict=products_dict)

@app.route('/searchcategory/<category>')
def searchcategory(category):
    db=shelve.open('user.db', 'c')
    products_dict={}
    product_list=[]
    try:
        if 'Products' in db:
            products_dict=db['Products']
        else:
            db['Products']=products_dict
    except:
        print("Error in retrieving Products from user.db.")
    db.close()
    if category=='electronic':
        for x, value in products_dict.items():
            if isinstance(value, Electronics.Electronics) and value.get_product_stock()>0:
                product_list.append(value)    
    elif category=='clothing':
        for x, value in products_dict.items():
            if isinstance(value, Clothing.Clothing) and value.get_product_stock()>0:
                product_list.append(value)  
    elif category=='accessories':
        for x, value in products_dict.items():
            if isinstance(value, Accessories.Accessories) and value.get_product_stock()>0:
                product_list.append(value)  
    return render_template("search.html", user=user, product_list=product_list)

@app.route('/search')
def search():
    term = request.args['search']
    db=shelve.open('user.db', 'c')
    products_dict={}
    product_list=[]
    try:
        if 'Products' in db:
            products_dict=db['Products']
        else:
            db['Products']=products_dict
    except:
        print("Error in retrieving Products from user.db.")
    db.close()
    for x, value in products_dict.items():
        if (term.lower() in value.get_name().lower()) and value.get_product_stock()>0:
            product_list.append(value)
    return render_template("search.html", user=user, product_list=product_list)

@app.route('/searchall')
def searchall():
    db=shelve.open('user.db', 'c')
    products_dict={}
    product_list=[]
    try:
        if 'Products' in db:
            products_dict=db['Products']
        else:
            db['Products']=products_dict
    except:
        print("Error in retrieving Products from user.db.")
    db.close()
    for x, value in products_dict.items():
        if value.get_product_stock()>0:
            product_list.append(value)
    return render_template("search.html", user=user, product_list=product_list)

@app.route('/ordernumber', methods=['GET', 'POST'])
def ordernumber():
    error=None
    order_number_form = f.OrderNumberForm(request.form)
    if request.method == 'POST' and order_number_form.validate():
        db = shelve.open('user.db', 'r')
        transactions_dict={}
        try:
            if 'Transactions' in db:
                transactions_dict=db['Transactions']
            else:
                db['Transactions']=transactions_dict
        except:
            print("Error in retrieving Transactions from user.db.")
        if not order_number_form.orderno.data in transactions_dict:
            error="Order Number does not exist"
        elif transactions_dict[order_number_form.orderno.data].get_delivered_date()!=0:
            error="Transaction already delivered"
        else:
            return redirect(url_for('tracking', order=order_number_form.orderno.data))
        db.close()
    return render_template('ordernumber.html', form=order_number_form, error=error, user=user)

@app.route('/tracking/<order>')
def tracking(order):
    db = shelve.open('user.db', 'r')
    transactions_dict={}
    try:
        if 'Transactions' in db:
            transactions_dict=db['Transactions']
        else:
            db['Transactions']=transactions_dict
    except:
        print("Error in retrieving Transactions from user.db.")
    transasction=transactions_dict[order]
    return render_template('tracking.html', user=user, transaction=transasction)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    error=None
    payment_form=f.PaymentForm(request.form)
    if request.method == 'POST' and payment_form.validate():
        payment_form.first_name.data = user.get_name()+user.get_last_name()
        creditlist=str(payment_form.creditcard.data)
        creditlist=[int(x) for x in creditlist]
        total=0
        for i, x in enumerate(creditlist[:-1]):
            if i%2==1:
                if x*2>9:
                    x=sum([int(y) for y in str(x*2)])
                    total+=x
                else:
                    total+=x*2
            else:
                total+=x
        if (10-(total%10))!=creditlist[-1]:
            error='Invalid credit card number'
        else:
            return redirect(url_for('transaction'))
    db = shelve.open('user.db', 'r')
    products_dict={}
    try:
        if 'Products' in db:
            products_dict=db['Products']
        else:
            db['Products']=products_dict
    except:
        print("Error in retrieving Products from user.db.")
    db.close()
    total_payment=0
    transaction_list= user.get_cart()
    for x in transaction_list:
        total_payment+=products_dict[x].get_price()
    product_list=[]
    for x in user.get_cart():
        product_list.append(products_dict[x])
    return render_template('transaction.html', user=user, total_payment=total_payment, product_list=product_list, form=payment_form, error=error)

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    db = shelve.open('user.db', 'c')
    products_dict={}
    try:
        if 'Products' in db:
            products_dict=db['Products']
        else:
            db['Products']=products_dict
    except:
        print("Error in retrieving Products from user.db.")
    for x in user.get_cart():
        products_dict[x].set_product_stock(products_dict[x].get_product_stock()-1)
    transaction=Transaction.Transaction(user.get_cart())
    for x in transaction.get_product_list():
        product=products_dict[x]
        product.set_sold(product.get_sold()+1)
        product.set_product_stock(product.get_product_stock()-1)
        products_dict[x]=product
    db['Products']=products_dict
    user.set_cart({})
    transactions_dict={}
    try:
        if 'Transactions' in db:
            transactions_dict=db['Transactions']
        else:
            db['Transactions']=transactions_dict
    except:
        print("Error in retrieving Transactions from user.db.")
    users_dict={}
    try:
        if 'Users' in db:
            users_dict=db['Users']
        else:
            db['Users']=users_dict
    except:
        print("Error in retrieving Users from user.db.")
    transactions_dict[transaction.get_id()]=transaction
    db['Transactions']=transactions_dict
    wishlist=user.get_transaction()
    wishlist[transaction.get_id()]=0
    user.set_transaction(wishlist)
    users_dict[user.get_user_id()]=user
    for x in transaction.get_product_list():
        seller = users_dict[products_dict[x].get_created_product()]
        earning=seller.get_earned()
        earning[d.date.today()]+=products_dict[x].get_price()
        seller.set_earned(earning)
    db['Users']=users_dict
    earning_dict={}
    try:
        if 'Earnings' in db:
            earning_dict=db['Earnings']
        else:
            db['Earnings']=earning_dict
    except:
        print("Error in retrieving Users from user.db.")
    total_payment=0
    for x in products_dict:
        total_payment+=products_dict[x].get_price()
    earning_dict[d.date.today()]+=total_payment
    db['Earnings']=earning_dict
    msg = Message("Transaction completed",
                  sender="chuaandspencer@example.com",
                  recipients=[user.get_email()])
    msg.body="Your transaction have been completed.\n\nYour Transaction order number is {}".format(transaction.get_id())
    mail.send(msg)
    db.close()
    return redirect(url_for('transactionsuccessful'))

@app.route('/transactionsuccessful')
def transactionsuccessful():
    return render_template("transactionsuccessful.html", user=user)

@app.route('/viewrefund')
def viewrefund():
    refund_dict={}
    product_dict = {}
    with shelve.open('user.db', 'c') as db:
        try:
            refund_dict = db['Refunds']
        except:
            print("Error in retrieving Customers from refund.db")
        try:
            product_dict = db['Products']
        except:
            print("Error in retrieving Customers from Product.db.")
        refund_list=[]
        if refund_dict!={}:
            for x in refund_dict:
                refund_list.append(refund_dict[x])
    while len(refund_list) < 5:
        refund_list.append(0)
    return render_template('viewrefund.html', refund_list=refund_list, user=user, product_dict=product_dict)

@app.route('/viewtransaction')
def viewtransaction():
    transaction_dict={}
    with shelve.open('user.db', 'c') as db:
        try:
            transaction_dict = db['Transactions']
        except:
            print("Error in retrieving Customers from transaction.db")
        transaction_list=[]
        if transaction_dict!={}:
            for x in transaction_dict:
                if transaction_dict[x].get_delivered_date()==0:
                    transaction_list.append(transaction_dict[x])
    while len(transaction_list) < 5:
        transaction_list.append(0)
    return render_template('viewdelivery.html', transaction_list=transaction_list, user=user)

@app.route('/refund/<int:id>')
def refund(id):
    refund_dict={}
    product_dict={}
    with shelve.open('user.db', 'c') as db:
        try:
            refund_dict = db['Refunds']
        except:
            print("Error in retrieving Customers from refund.db.")
        try:
            product_dict = db['Products']
        except:
            print("Error in retrieving Customers from refund.db.")
        refund=refund_dict[id]
    return render_template('refund.html', refund=refund, user=user, product_dict=product_dict)

@app.route('/changestatus/<id>')
def changestatus(id):
    with shelve.open('user.db', 'c') as db:
        try:
            transaction_dict = db['Transactions']
        except:
            print("Error in retrieving Customers from transaction.db.")
        transaction=transaction_dict[id]
    return render_template('changestatus.html', transaction=transaction, user=user)

@app.route('/addstatus/<id>')
def addstatus(id):
    db = shelve.open('user.db', 'c')
    transactions_dict={}
    try:
        if 'Transactions' in db:
            transactions_dict=db['Transactions']
        else:
            db['Transactions']=transactions_dict
    except:
        print("Error in retrieving Transactions from user.db.")
    transaction=transactions_dict[id]
    transaction.set_status(transaction.get_status()+1)
    transactions_dict[id]=transaction
    db['Transactions']=transactions_dict
    db.close()
    return redirect(url_for('changestatus', id=id))

@app.route('/removestatus/<id>')
def removestatus(id):
    db = shelve.open('user.db', 'c')
    transactions_dict={}
    try:
        if 'Transactions' in db:
            transactions_dict=db['Transactions']
        else:
            db['Transactions']=transactions_dict
    except:
        print("Error in retrieving Transactions from user.db.")
    transaction=transactions_dict[id]
    transaction.set_status(transaction.get_status()-1)
    transactions_dict[id]=transaction
    db['Transactions']=transactions_dict
    db.close()
    return redirect(url_for('changestatus', id=id))

@app.route('/compare/<int:id>/<int:id2>')
def compare(id, id2):
    product_dict = {}
    with shelve.open('user.db', 'c') as db:
        try:
            product_dict = db['Products']
        except:
            print("Error in retrieving Customers from Product.db.")
    x=product_dict[id]
    y=product_dict[id2]
    if isinstance(x, Electronics.Electronics):
        return render_template('compareelectronic.html', x=x,y=y, user=user)
    if isinstance(x, Clothing.Clothing):
        return render_template('compareclothing.html', x=x,y=y, user=user)
    if isinstance(x, Accessories.Accessories):
        return render_template('compareaccessories.html', x=x,y=y, user=user)
    
@app.route('/comparesecond/<int:id>', methods=['GET', 'POST'])
def comparesecond(id):
    if request.method == 'POST':
        id2=request.form.get('wishlistitems')
        return redirect(url_for('compare', id=id, id2=id2))
    product_dict = {}
    with shelve.open('user.db', 'c') as db:
        try:
            product_dict = db['Products']
        except:
            print("Error in retrieving Customers from Product.db.")
    x=product_dict[id]
    product_list=[]
    if isinstance(x,Electronics.Electronics):
        for i, y in product_dict.items():
            if isinstance(y,Electronics.Electronics) and i!=x.get_product_id():
                product_list.append(y)
    if isinstance(x,Clothing.Clothing):
        for i, y in product_dict.items():
            if isinstance(y,Clothing.Clothing) and i!=x.get_product_id():
                product_list.append(y)
    if isinstance(x,Accessories.Accessories):
        for i, y in product_dict.items():
            if isinstance(y,Accessories.Accessories) and i!=x.get_product_id():
                product_list.append(y)
    
    return render_template('comparesecond.html', x=x, user=user, product_list=product_list)

@app.route('/approverefund/<int:id>/<transaction_id>/<int:product_id>')
def approverefund(id, transaction_id, product_id):
    refund_dict = {}
    user_dict = {}
    product_dict = {}
    transaction_dict = {}
    earning_dict = {}
    with shelve.open('user.db', 'c') as db:
        try:
            refund_dict = db['Refunds']
        except:
            print("Error in retrieving Customers from staff.db.")
        try:
            user_dict = db['Users']
        except:
            print("Error in retrieving Customers from staff.db.")
        try:
            product_dict = db['Products']
        except:
            print("Error in retrieving Customers from staff.db.")
        try:
            transaction_dict = db['Transactions']
        except:
            print("Error in retrieving Customers from staff.db.")
        try:
            earning_dict = db['Earnings']
        except:
            print("Error in retrieving Customers from staff.db.")
        refund=refund_dict[id] 
        msg = Message("Refund approved",
                  sender="chuaandspencer@example.com",
                  recipients=[user_dict[refund.get_refund_by()].get_email()])
        msg.body="Your refund for item {} have been approved.".format(product_dict[refund.get_product_name()])
        mail.send(msg)
        transaction_dict[transaction_id].set_product_list(transaction_dict[transaction_id].get_product_list().pop(product_id))
        refund_dict.pop(id)
        product=product_dict[product_id]
        earning_dict[d.date.today()]-=product.get_price()*0.1
        seller=user_dict[product.get_created_product()]
        earning=seller.get_earned()
        earning[d.date.today()]-=product.get_price()*0.9
        seller.set_earned(earning)
        user_dict[seller.get_seller_id()]=seller
        db['Refunds'] = refund_dict
        db['Transactions'] = transaction_dict
        db['Earnings'] = earning_dict
        db['Users'] = user_dict
        return redirect(url_for('viewrefund'))
    
@app.route('/rejectrefund/<int:id>')
def rejectrefund(id):
    refund_dict = {}
    user_dict = {}
    product_dict = {}
    with shelve.open('user.db', 'c') as db:
        try:
            refund_dict = db['Refunds']
        except:
            print("Error in retrieving Customers from staff.db.")
        try:
            user_dict = db['Users']
        except:
            print("Error in retrieving Customers from staff.db.")
        try:
            product_dict = db['Products']
        except:
            print("Error in retrieving Customers from staff.db.")
        refund=refund_dict[id] 
        msg = Message("Refund rejected",
                  sender="chuaandspencer@example.com",
                  recipients=[user_dict[refund.get_refund_by()].get_email()])
        msg.body="Your refund for item {} have been rejected.".format(product_dict[refund.get_product_name()])
        mail.send(msg)
        refund_dict.pop(id)
        db['Refunds'] = refund_dict
        return redirect(url_for('viewrefund'))

@app.route('/processrefund')
def processrefund():
    id=int(request.args.get('id'))
    reason=request.args.get('reason')
    transaction_id=request.args.get('transaction_id')
    db=shelve.open('user.db', 'c')
    refunds_dict={}
    try:
        if 'Refunds' in db:
            refunds_dict=db['Refunds']
        else:
            db['Refunds']=refunds_dict
    except:
        print("Error in retrieving Transactions from user.db.")
    refund=Refund.Refund(id,reason,user.get_user_id(), transaction_id)
    refunds_dict[refund.get_id()] = refund
    db['Refunds'] = refunds_dict
    db.close()
    return redirect(url_for("refundsuccessful"))

@app.route('/finishdelivery/<id>')
def finishdelivery(id):
    db=shelve.open('user.db', 'c')
    transactions_dict={}
    try:
        if 'Transactions' in db:
            transactions_dict=db['Transactions']
        else:
            db['Transactions']=transactions_dict
    except:
        print("Error in retrieving Transactions from user.db.")
    transaction=transactions_dict[id]
    transaction.set_delivered_date(d.date.today())
    db['Transactions']=transactions_dict
    db.close()
    return redirect(url_for("viewtransaction", user=user))

@app.route('/refundsuccessful')
def refundsuccessful():
    return render_template("refundsuccessful.html", user=user)

if __name__ == '__main__':
    import webbrowser

    webbrowser.open("http://127.0.0.1:5000/")
    app.run()
