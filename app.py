from flask import Flask, render_template, request
from mysql.connector import connect

app = Flask(__name__)

db=connect(host='localhost', user='root', passwd='', database='Uchumi')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/products')
def products():
    items = ['unga','sugar','milk','eggs','pens','books']
    return render_template('products.html', items_products=items)


@app.route('/contact')
def contact():
    return render_template('contact.html')


# names, quantity, price
@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        print(request.form)
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        print(name, quantity, price)
        cursor = db.cursor()
        sql ='insert into products values(null, %s,%s,%s)'
        data = (name, quantity, price)
        cursor.execute(sql,data)
        db.commit()

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
