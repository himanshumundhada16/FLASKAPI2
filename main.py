from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aiind8852*@localhost/flaskapi'
app.debug = True
db = SQLAlchemy(app)
ma = Marshmallow(app)


class students(db.Model):
    __tablename__ = "studentinfo"
    sid = db.Column(db.Integer(), primary_key=True, nullable=False)
    sname = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def __init__(self, sid, sname, role):
        self.sid = sid
        self.sname = sname
        self.role = role


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('sid', 'sname', 'role')


student_schema = StudentSchema()


@app.route('/', methods=['GET'])
def hello():
    return jsonify({'msg': 'Hello, Welcome !'})


@app.route('/student', methods=['GET'])
def getstudents():
    allStudents = students.query.all()
    output = []
    for student in allStudents:
        currStudent = {}
        currStudent['sid'] = student.sid
        currStudent['sname'] = student.sname
        currStudent['role'] = student.role
        output.append(currStudent)
    return jsonify(output)


@app.route('/student', methods=['POST'])
def poststudents():
    studentData = request.get_json()
    student = students(sid=studentData['sid'], sname=studentData['sname'], role=studentData['role'])
    db.session.add(student)
    db.session.commit()
    return jsonify(studentData)


@app.route('/student/<sid>', methods=['GET'])
def get_student(sid):
    student = students.query.get(sid)
    return student_schema.jsonify(student)
