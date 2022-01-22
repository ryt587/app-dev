from flask import Flask, render_template,  request, redirect, url_for, Response
import Forms as f
import shelve, Customer, Apply, Staff, Seller, Electronics, Clothing
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from uuid import uuid4
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY']=uuid4().hex
app.config['UPLOAD_PATH'] = 'static/images/cert/'
app.config['UPLOAD_FOLDER'] = 'static/images/product_image/'
app.config["ALLOWED_IMAGE_EXTENSIONS"]=['png', 'jpg', 'jpeg']
app.config['MAIL_USERNAME'] = 'chuaandpencer@gmail.com'
app.config['MAIL_PASSWORD'] = 'nypappdev2022'
app.config['MAIL_DEFAULT_SENDER'] = 'chuaandpencer@gmail.com'

mail=Mail(app)

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
        with shelve.open('user.db', 'c') as db:
            try:
                if 'Applications' in db:
                    applications_dict = db['Applications']
                else:
                    db['Applications'] = applications_dict
            except:
                print("Error in retrieving Customers from application.db.")
            if not allowed_image(file.filename):
                    error="Missing image or invalid format of image"
                    no_of_error+=1
            elif applications_dict!={}:
                for x in applications_dict:
                    if  create_seller_form.email.data==applications_dict[x].get_email():
                        error="Email has been used before"
                        no_of_error+=1
                        break
            if no_of_error==0:
                application = Apply.Apply(create_seller_form.name.data, create_seller_form.email.data, create_seller_form.password.data, create_seller_form.address.data,
                                        create_seller_form.address2.data, create_seller_form.city.data, create_seller_form.postal.data, file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(file.filename)))
                applications_dict[application.get_apply_id()] = application
                db['Applications'] = applications_dict
                return redirect(url_for('home'))
    return render_template('sellerapplication.html', form=create_seller_form, error=error, user=user)


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
                Product = Electronics.Electronics(create_product_form.Product_name.data, create_product_form.Product_stock.data, file.filename, user.get_seller_id(),
                                                  create_product_form.Electronics_gpu.data, create_product_form.Electronics_cpu.data,
                                                  create_product_form.Electronics_storage.data, create_product_form.Electronics_memory.data,
                                                  create_product_form.Electronics_size.data)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                product_dict[Product.get_product_id()] = Product
                db['Products'] = product_dict
                return redirect(url_for('seller'))
    return render_template('electronic_products.html', form=create_product_form, error=error, user=user)

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
                Product = Clothing.Clothing(create_product_form.Product_name.data, create_product_form.Product_stock.data, file.filename, user.get_seller_id(),
                                            create_product_form.Clothing_colour.data, create_product_form.Clothing_size.data)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
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
        update_product_form.Clothing_colour.data = product.get_colour()
        update_product_form.Clothing_size.data = product.get_size()

        return render_template('updateclothing.html', form=update_product_form, user=user)


@app.route('/deleteproduct/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('user.db', 'w')
    products_dict = db['Products']
    product=products_dict[id]
    os.remove(app.config['UPLOAD_FOLDER']+str(product.get_product_image()))
    products_dict.pop(id)

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
    with shelve.open('user.db', 'c') as db:
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

    users_dict.pop(user.get_seller_id())

    db['Users'] = users_dict
    db.close()

    user=0

    return redirect(url_for('home'))

@app.route('/reportseller')
def reportseller():
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
                productlist.append(users_dict[x])
    def byimpression(product):
        return product.get_impression()
    productlist=sorted(productlist, key= byimpression)
    db.close()
    return render_template('reportseller.html', user=user, productlist=productlist)

@app.route('/reportstaff')
def reportstaff():
     # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([x for x in range(31)],)
    # Save it to a temporary buffer.
    output = BytesIO()
    # Embed the result in the html output.
    FigureCanvasAgg(fig).print_png(output)

if __name__ == '__main__':
    import webbrowser

    webbrowser.open("http://127.0.0.1:5000/")
    app.run()
