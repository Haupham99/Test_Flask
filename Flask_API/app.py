from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class students(db.Model):
    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50)) 
    addr = db.Column(db.String(200)) 
    pin = db.Column(db.String(10))

    def update(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

@app.route('/')
def show_all():
   return render_template('show_all.html', students = students.query.all() )

@app.route('/create', methods = ['GET', 'POST'])
def create():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],
            request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('create.html')

@app.route('/update/<id>', methods = ['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        stu = students.query.get(id)
        stu.name = request.form['name']
        stu.city = request.form['city']
        stu.addr = request.form['addr']
        stu.pin = request.form['pin']

        db.session.commit()
        flash('Update successfully')
        return redirect(url_for('show_all'))
    return render_template('update.html', data = students.query.get(id))

@app.route('/delete/<id>')
def delete(id):
   stu = students.query.get(id)
   db.session.delete(stu)
   db.session.commit()

   return redirect(url_for('show_all'))

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)