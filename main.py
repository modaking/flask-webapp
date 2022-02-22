import re, os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from flask_principal import Principal
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Modda/PycharmProjects/Web database/Test3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Secret key'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role_id != 1:
            flash('You are not authorised', 'warning')
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return decorated_view


class User(db.Model, UserMixin):
    username = db.Column('username', db.String(80), unique=True, nullable=False)
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(100), unique=True, nullable=False)
    password = db.Column('password', db.String(150), nullable=False)
    date_added = db.Column('date_added', db.DateTime, default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    active = db.Column('active', db.Boolean, default=True)


class Role(db.Model):
    name = db.Column('name', db.String(25), unique=True, nullable=False)
    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    Users = db.relationship('User', backref='users')


"""
a = Role(name='Admin')
b = Role(name='Employee')
c = Role(name='User')


db.session.add_all([a,b,c])
db.session.commit()
#db.session.rollback()
#db.session.commit()
"""

"""
email1 = 'ModaKing@gmail.com'
email3 = 'Aphrodite@gmail.com'
email2 = 'Ian9toz@gmail.com'
password_1 = 'Bongcloud'
password_2 = 'Fianchetto'
password_3 = 'Estoy_loco'

user_1 = User(username='Moda',email=email1, password=generate_password_hash(password_1,method='sha256'),role_id=1)
user_2 = User(username='Iantoz',email=email2, password=generate_password_hash(password_2,method='sha256'),role_id=1)
user_3 = User(username='Aphrodite',email=email3, password=generate_password_hash(password_3,method='sha256'),role_id=1)


db.session.add_all([user_1,user_2,user_3])
db.session.commit()


"""

"""
email1= 'Crossbones@gmail.com'
email2= 'Biggiesmalls@gmail.com'
email3= 'Dawn@gmail.com'
email4= 'Tupac_Shakur@gmail.com'


password_1 ='Valor_Morghulis'
password_2 ='Juicy'
password_3 ='Amore'
password_4 = 'Westcoast'

user_1 = User(username='Cross',email=email1, password=generate_password_hash(password_1,method='sha256'),role_id=2)
user_2 = User(username='Biggie',email=email2, password=generate_password_hash(password_2,method='sha256'),role_id=2)
user_3 = User(username='Dawn',email=email3, password=generate_password_hash(password_3,method='sha256'),role_id=2)
user_4 = User(username='Tupac',email=email4, password=generate_password_hash(password_4,method='sha256'),role_id=2)


db.session.add_all([user_1,user_2,user_3,user_4])
db.session.commit()
"""


x = User.query.filter_by(role_id=1).all()

for i in x:
    print(str(i.date_added))
    # db.session.delete(i)
    # db.session.commit()

x = Role.query.all()
for i in x:
    print("\n\n" + i.name, "|" + str(i.Users) + "\n")
    for e in i.Users:
        print(e.email, " | " + str(e.id), " | " + e.username, " | " + str(e.date_added), " | " + e.password)

print('Thanks')


product_tag = db.Table('product_tag',
        db.Column('product_id', db.Integer, db.ForeignKey('product.product_id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'))
)


class Product(db.Model):
    product_id = db.Column('product_id', db.Integer, primary_key=True)
    file_path = db.Column('file_path', db.String(), nullable=False)
    product_name = db.Column('product_name', db.String(80),nullable=False)
    product_variations = db.relationship('Variation', backref= 'product')
    product_category = db.Column('product_category', db.String(50), nullable=False)
    product_description = db.Column('product_description', db.Text, nullable=False)
    product_price = db.Column('price', db.Integer,nullable=False)
    product_tags = db.relationship('Tag', secondary = product_tag, backref = 'product')
    date_added = db.Column('date_added', db.DateTime, default=datetime.utcnow)  
    

class Variation(db.Model):
    id = db.Column('var_id', db.Integer, primary_key=True)
    file_path = db.Column('file_path', db.String())
    parent_product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'))


class Tag(db.Model):
    id = db.Column('tag_id', db.Integer, primary_key=True)
    tag = db.Column('tag', db.String(25), nullable=False, unique=True)


class Employee(db.Model):
    employee_name = db.Column('employee_name', db.String(100))
    employee_id = db.Column('employee_id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer())
    department_name = db.Column('department', db.ForeignKey('department.name'))


class Department(db.Model):
    name = db.Column('name', db.String(25), unique=True, nullable=False)
    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    employees = db.relationship('Employee', backref='employee')


"""
class Orders(db.Model):
    customer_name= db.Column('customer_name', db.String(100), nullable=False)
    customer_id= db.Column('customer_id', db.Integer, nullable=False)
    ordered_products = db.relationship('Ordered_products', backref='ordered_products')
    order_id = db.Column('order_id', db.Integer, primary_key=True)
    total_quantities = db.Column('quantity', db.Integer)
    total_amount = db.Column('total_amount', db.Integer)
    location = db.Column('delivery_location', db.String(100))
    status = db.Column('delivery_status', db.Boolean)
    order_date = db.Column('order_date',db.DateTime, default=datetime.utcnow)
 
    
class Ordered_products(db.Model):
    row_id = db.Column('row_id', db.Integer, primary_key=True)
    product_name = db.Column('product_name', db.String(100), nullable=False)
    product_id = db.Column('product_id', db.Integer nullable=False)
    quantities = db.Column('quantity', db.Integer(),nullable=False)
    total_price = db.Column('total_price',db.Integer,nullable=False)
    parent_order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))


class Sales(db.Model):
    prod_name = db.Column('product_name', db.String(100), nullable=False)
    purchases_quantity = db.Column('purchases_quantity', db.Integer, default=0)
    returns_quantity = db.Column('returns_quantity', db.Integer, default=0)
    revenue = db.Column('revenue', db.Integer, default=0)
    category_id = db.Column('category_id', db.Integer, primary_key=True)

"""


@app.route('/')
@login_required
def index():
    path = 'static/images/'
    images = os.listdir(path)
    route = [file for file in images]
    images = ['images/' + file for file in images]
    print(images)
    return render_template("index.html", images=images)


@app.route('/description/<directory>/<filename>')
@login_required
def description(directory, filename):
    print(filename)
    path = directory + '/' + filename
    print(path)
    return render_template("description.html", path=path)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("Username")
        email = request.form.get("Email")
        password = request.form.get("password")
        confirm_password = request.form.get("Confirm_password")

        pattern = '[a-z A-Z 0-9]+@[a-zA-Z]+\.(com|edu|net)$'

        if not username:
            flash('Please enter Username')
            return redirect(url_for('sign_up'))
        elif not email:
            flash(" Please enter Email")
            return redirect(url_for('sign_up'))
        elif not password:
            flash('Please enter Password')
            return redirect(url_for('sign_up'))
        elif not confirm_password:
            flash('Please enter Password confirmation')
            return redirect(url_for('sign_up'))
        elif password != confirm_password:
            flash("Password does not match password confirmation")
            return redirect(url_for('sign_up'))
        elif len(password) <= 7:
            flash('Password is too short.At least 8 characters required')
            return redirect(url_for('sign_up'))
        elif len(email) <= 4:
            flash('Email is too short')
            return redirect(url_for('sign_up'))
        elif not (re.search(pattern, email)):
            flash('Invalid email')
            return redirect(url_for('sign_up'))
        else:
            username_exists = User.query.filter_by(username=username).first()

            email_exists = User.query.filter_by(email=email).first()

            if username_exists:
                flash('Username already exists')
                return redirect(url_for('sign_up'))

            elif email_exists:
                flash('Email already has an account. Please login to account')
                return redirect(url_for('login'))

            else:
                new_user = User(email=email, username=username,
                                password=generate_password_hash(password, method='sha256'),
                                role_id=3)

                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=False)
                y = User.query.all()
                for i in y:
                    if i.email:
                        print(i.id, ' | ' + i.username, ' | ' + i.email, ' | ' + i.password, '|' + str(i.role_id))

                flash('Welcome '+username)
                return redirect(url_for('index'))

    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("Username")
        password = request.form.get("password")
        if not username:
            flash('Please enter a username')
            return redirect(url_for('login'))
        elif not password:
            flash('Please enter Password')
            return redirect(url_for('login'))
        else:
            y = User.query.filter_by(username=username).first()
            if y:
                if check_password_hash(y.password, password):
                    login_user(y, remember=False)

                    if current_user.role_id == 1:
                        flash('Welcome Admin '+username)
                        return redirect(url_for('index'))
                    elif current_user.role_id == 2:
                        flash('Welcome Employee ' + username)
                        return redirect(url_for('index'))
                    else:
                        flash('Welcome ' + username)
                        return redirect(url_for('index'))
                else:
                    flash('Please enter correct password')
                    return redirect(url_for('login'))
            else:
                flash('Please enter a valid username')
                return redirect(url_for('login'))

    return render_template("login.html")


@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
    return render_template("admin.html")


@app.route('/admin_employees', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_employees():
    
    if request.method == 'POST':
        username = request.form.get("Username")
        email = request.form.get("Email")
        password = request.form.get("password")
        department = request.form.get("department")

        pattern = '[a-z A-Z 0-9]+@[a-zA-Z]+\.(com|edu|net)$'

        if not username:
            flash('Please enter Username')
            return redirect(url_for('admin_employees'))
        elif not email:
            flash(" Please enter Email")
            return redirect(url_for('admin_employees'))
        elif not password:
            flash('Please enter Password')
            return redirect(url_for('admin_employees'))
        elif not department:
            flash('Please choose department')
            return redirect(url_for('admin_employees'))
        elif len(password) <= 7:
            flash('Password is too short.At least 8 characters required')
            return redirect(url_for('admin_employees'))
        elif len(email) <= 4:
            flash('Email is too short')
            return redirect(url_for('admin_employees'))
        elif not (re.search(pattern, email)):
            flash('Invalid email')
            return redirect(url_for('admin_employees'))
        else:
            username_exists = User.query.filter_by(username=username).first()

            email_exists = User.query.filter_by(email=email).first()

            if username_exists:
                flash('Username already exists')
                return redirect(url_for('admin_employees'))

            elif email_exists:
                flash('Email already has an account. Please login to account')
                return redirect(url_for('admin_employees'))

            else:
                new_user = User(email=email, username=username,
                                password=generate_password_hash(password, method='sha256'),
                                role_id=2)

                db.session.add(new_user)
                db.session.commit()

                x = User.query.filter_by(email=email).first()

                new_employee = Employee(employee_name=username, user_id=x.id, department_name=department)

                db.session.add(new_employee)
                db.session.commit()

                login_user(new_user, remember=False)
                flash('Employee ' + username + 'added')
                return redirect(url_for('admin_employees'))

    return render_template("admin_employees.html")


@app.route('/admin_noticeboard', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_noticeboard():
    return render_template("admin_noticeboard.html")


app.config['UPLOAD_PATH'] = 'static/images'


@app.route('/admin_product', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_product():
    
    if request.method == 'POST':
        product = request.files["Product"]
        variations = request.files.getlist("Variations[]")
        name = request.form.get("Name")
        category = request.form.get("Category")
        price = request.form.get("Price")
        tags = request.form.get("Tags")
        desc = request.form.get("Description")
        print(variations)

        if not product:
            flash('Please add a product file')
            return redirect(url_for('admin_product'))
        elif not variations:
            flash(" Please enter product variations files")
            return redirect(url_for('admin_product'))
        elif not name:
            flash("Please enter Product's name")
            return redirect(url_for('admin_product'))
        elif not category:
            flash("Please enter Product's category")
            return redirect(url_for('admin_product'))

        elif not price:
            flash(" Please enter Product's price")
            return redirect(url_for('admin_product'))
        elif not desc:
            flash("Please enter Product's description")
            return redirect(url_for('admin_product'))
        else:
            prodname = secure_filename(product.filename)
            prodpath = os.path.join(app.config['UPLOAD_PATH'], prodname)

            new_product = Product(file_path=prodpath, product_name=name, product_category=category, product_price=price, product_description=desc)
            db.session.add(new_product)
            db.session.commit()
            if tags:
                for a in tags:
                    d = Tag.query.filter_by(tag=a).first()
                    if x:
                        new_product.product_tags.append(d.tag)
                    else:
                        new_tag = Tag(tag=a)

                        db.session.add(new_tag)
                        db.session.commit()

                        new_product.product_tags.append(a)

            z = Product.query.filter_by(filepath=prodpath).first()

            for file in variations:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_PATH'], filename)
                new_var = Variation(file_path=filepath, parent_product_id=z.id)
                db.session.add(new_var)
                db.commit()
                file.save(filepath)

    return render_template("admin_product.html")


@app.route('/admin_users', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_users():
    return render_template("admin_users.html")


@app.route('/admin_data', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_data():
    return render_template("admin_users.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out Successfully')
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)
