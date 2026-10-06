from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# flash() ke liye zaroori hai
app.secret_key = "change-this-to-a-random-string"

db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()



@app.route("/")
def display_employee_data():
    employees = Employee.query.all()
    return render_template("empdata.html", empdata=employees)



@app.route("/addemp", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        employee = Employee(
            id=request.form["id"],
            name=request.form["nm"],
            email=request.form["email"],
            salary=request.form["sal"],
        )
        db.session.add(employee)
        db.session.commit()

    
        flash("Employee added successfully!", "success")
        return redirect("/")

    return render_template("add_employee.html")



@app.route("/updateemp/<int:id>", methods=["GET", "POST"])
def update_employee(id):
    employee = db.get_or_404(Employee, id)

    if request.method == "POST":
        employee.name = request.form["nm"]
        employee.email = request.form["email"]
        employee.salary = request.form["sal"]
        db.session.commit()

        return render_template(
            "editemployee.html",
            employee=employee,
            message="Employee Data Updated Successfully",
        )

    return render_template("editemployee.html", employee=employee)



@app.route("/deleteemp/<int:id>", methods=["GET", "POST"])
def delete_employee(id):
    employee = db.get_or_404(Employee, id)

    if request.method == "POST":
        db.session.delete(employee)
        db.session.commit()
        flash("Employee deleted successfully!", "success")
        return redirect("/")

    return render_template("deleteemployee.html", employee=employee)


if __name__ == "__main__":
    app.run(debug=True)