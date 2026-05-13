from flask import Flask, render_template
from flask import request, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"

db = SQLAlchemy(app)

class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    age = db.Column(
        db.Integer
    )

    major = db.Column(
        db.String(100)
    )

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        major = request.form["major"]

        student = Student(
            name=name,
            age=age,
            major=major
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/")

    students = Student.query.all()

    return render_template(
        "index.html",
        students=students
    )

@app.route("/delete/<int:id>")
def delete(id):

    student = Student.query.get(id)

    db.session.delete(student)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
