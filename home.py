from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(250), nullable = False)
    desc = db.Column(db.String(1000), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
         return f"{self.id} - {self.task}"
 

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':#
        task = request.form['task']#
        desc = request.form['desc']#
        todo = Todo(task=task, desc=desc)#
        db.session.add(todo)#
        db.session.commit()#
    # todo = Todo(task="TASK1", desc="DESC1")
    # db.session.add(todo)
    # db.session.commit()

    allTodo = Todo.query.all()
    return render_template("home.html", allTodo = allTodo)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method =='POST':
        task = request.form['task']
        desc = request.form['desc']
        todo_item = Todo.query.filter_by(id=id).first()
        todo_item.task = task
        todo_item.desc = desc
        db.session.add(todo_item)
        db.session.commit()
        return redirect("/")
    
    todo_item = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo_item = todo_item)
 
@app.route('/delete/<int:id>')
def delete(id):
    todo_item = Todo.query.filter_by(id=id).first()
    db.session.delete(todo_item)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)
