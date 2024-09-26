from init import db, ma

class Employee(db.Model):
    __tablename__ = "Employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)

class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


