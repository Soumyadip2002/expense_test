from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

conn=mysql.connector.connect(host='localhost',user='root',passwd='Riky@1234',database='riky')
cursor=conn.cursor()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/expenses")
def expenses():

    cursor.execute("""select CategoryID,CategoryName from category""")
    categories=cursor.fetchall()
    print(categories)
    return render_template('expenses.html',categories=categories)

@app.route("/add_expense" , methods=['POST'])
def add_expense():
    try:
        amount=request.form.get('amount')
        desc=request.form.get('desc')
        category_name=request.form.get('category_name')
        datepicker=request.form.get('datepicker')

        cursor.execute("""INSERT INTO `EXPENSES` (`categoryid`,`Amount`,`ExpenseDate`,`ExpenseDesc`) values
                       (%s,%s,%s,%s) """,(category_name,amount,datepicker,desc))

        conn.commit()
    except Exception as e:
        return f'<h1>Error: {str(e)}</h1>',500
    # return 'Expense Created Successfully!!'
    return render_template('expenses.html')

@app.route("/expense_view")
def expense_view():
    cursor.execute("""select e.ExpenseDate, e.Amount, e.ExpenseDesc, c.categoryname from expenses e join category c on e.categoryid=c.categoryid order by e.ExpenseDate desc""")
    expense_all=cursor.fetchall()
    # print(expense_all)

    return render_template('expense_view.html',expense_all=expense_all)

if __name__=='__main__':
    app.run(debug=True)
