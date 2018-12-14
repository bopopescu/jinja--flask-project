from flask import Flask, render_template, request, redirect, url_for, flash, session
from mysql.connector import connect
# app.config['SECRET_KEY'] ='29f839c55ccb8a484afade90ac0b44f6'
app = Flask(__name__)

db = connect(host='localhost', user='root', passwd='', database='Uchumi')
app.secret_key = 'ghjwiwiuwnskwdks'


@app.route('/')
def home():
    if session.get('id') is None:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/products')
def products():
    if session.get('id') is None:
        return redirect(url_for('login'))
    sql = 'select * from products'
    cursor = db.cursor()
    cursor.execute(sql)
    products = cursor.fetchall()
    print(products)

    items = ['unga', 'sugar', 'milk', 'eggs', 'pens', 'books']
    return render_template('products.html', items_products=items, products=products)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/delete/<id>')
def delete(id):
    if session.get('id') is None:
        return redirect(url_for('login'))
    sql = 'delete from products where pid= %s'
    data = (id,)
    cursor = db.cursor()
    cursor.execute(sql, data)
    db.commit()
    flash('Deleted successfully','text-danger')
    return redirect(url_for('products'))


# names, quantity, price

@app.route('/add', methods=['POST', 'GET'])
def add():
    if session.get('id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('form.html')
    else:
        print(request.form)
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        print(name, quantity, price)
        cursor = db.cursor()
        sql = 'insert into products values(null, %s,%s,%s)'
        data = (name, quantity, price)
        cursor.execute(sql, data)
        db.commit()
    flash('Added product successfully')
    return render_template('form.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    if session.get('id') is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('add_user.html')
    else:
        print(request.form)
        names = request.form['names']
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        sql = 'insert into users values(null, %s,%s,%s)'
        data = (names, email, password)
        cursor.execute(sql, data)
        db.commit()
    flash('added user successfully','text-info')
    return render_template('add_user.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(request.form)

        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        sql = 'select * from users where email=%s and password=%s'
        data = (email, password)
        cursor.execute(sql, data)
        user = cursor.fetchone()
        print(user)
        if user == None:
            flash('Wrong email or password')
            return redirect(url_for('login'))
        else:
            session['id'] = user[0]
            session['names'] = user[1]
            session['email'] = user[2]
            flash('logged in successfully','text-info')
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    if session.get('id') == None:
        return redirect(url_for('login'))
    session.clear()
    flash('logged out successfully','text-info')
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
