from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable = False)
    data_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo=allTodo)
    # return "<p>Hello, world!</p>"


@app.route("/products")
def products():
    return "<p>products page</p>"

@app.route("/update")
def update():
    return "Good"

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port = 8000)