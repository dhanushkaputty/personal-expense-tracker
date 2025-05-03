from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/expense_tracker"
mongo = PyMongo(app)

@app.route('/')
def index():
    expenses = list(mongo.db.expenses.find().sort("date", -1))
    for expense in expenses:
        expense['_id'] = str(expense['_id'])  # Convert ObjectId to string
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        type_ = request.form['type']
        category = request.form['category']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        mongo.db.expenses.insert_one({
            'title': title,
            'amount': amount,
            'type': type_,
            'category': category,
            'date': date
        })
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/update/<id>', methods=['GET', 'POST'])
def update_expense(id):
    expense = mongo.db.expenses.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        mongo.db.expenses.update_one({'_id': ObjectId(id)}, {
            '$set': {
                'title': request.form['title'],
                'amount': float(request.form['amount']),
                'type': request.form['type'],
                'category': request.form['category'],
                'date': datetime.strptime(request.form['date'], '%Y-%m-%d')
            }
        })
        return redirect(url_for('index'))
    return render_template('update_expense.html', expense=expense)

@app.route('/delete/<id>')
def delete_expense(id):
    mongo.db.expenses.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
