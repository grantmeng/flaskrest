#!/usr/bin/python3

from flask import Flask, request, jsonify
from config import *
from models import db, Person, Student, Tutor, Course, Class
from errors import InvalidUsage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Class Course API</h1><li>Persons</li><li>Students</li><li>Tutors</li><li>Courses</li><li>Classes</li>'

@app.route('/persons/')
def persons():
    try:
        args = request.args
        res = []
        for row in Person.query.filter_by(**args):
            row = row.to_dict()
            row['role'] = ''
            if Student.query.get(row['id']): row['role'] = 'Student'
            if Tutor.query.get(row['id']): row['role'] = 'Tutor'
            res.append(row)
        return jsonify(res)
    except Exception as e:
        print(e)
        raise InvalidUsage('Invalid query string', status_code=410, payload={'payload': 'Please check the query string'})

@app.route('/persons/<int:id>')
def person(id):
    res = Person.query.get(id)
    if res:
        res = res.to_dict()
        res['role'] = ''
        if Student.query.get(res['id']): res['role'] = 'Student'
        if Tutor.query.get(res['id']): res['role'] = 'Tutor'
    return jsonify(res)

@app.route('/students/')
def students():
    try:
        args = request.args
        res = Student.query.filter_by(**args)
        res = list(row.to_dict() for row in res)
        return jsonify(res)
    except Exception as e:
        print(e)
        raise InvalidUsage('Invalid query string', status_code=410)

@app.route('/students/<int:id>')
def student(id):
    res = Student.query.get(id)
    if res: res = res.to_dict()
    return jsonify(res)

@app.route('/tutors/')
def tutors():
    try:
        args = request.args
        res = Tutor.query.filter_by(**args)
        res = list(row.to_dict() for row in res)
        return jsonify(res)
    except Exception as e:
        print(e)
        raise InvalidUsage('Invalid query string', status_code=410)

@app.route('/tutors/<int:id>')
def tutor(id):
    res = Tutor.query.get(id)
    if res: res = res.to_dict()
    return jsonify(res)

@app.route('/courses/')
def courses():
    try:
        args = request.args
        res = []
        for row in Course.query.filter_by(**args).join(Person, Person.id==Course.tutor_id).add_columns(Person.lastname, Person.firstname):
            lastname, firstname = row.lastname, row.firstname
            row = row.Course.to_dict()
            row['tutor_name'] = '{} {}'.format(firstname, lastname)
            row['tutor_url'] = '{}tutors/{}'.format(request.url_root, row['tutor_id'])
            res.append(row)
        return jsonify(res)
    except Exception as e:
        print(e)
        raise InvalidUsage('Invalid query string', status_code=410)

@app.route('/courses/<int:id>')
def course(id):
    res = Course.query.get(id)
    if res:
        person = Person.query.get(res.tutor_id)
        res = res.to_dict()
        res['tutor_name'] = '{} {}'.format(person.firstname, person.lastname)
        res['tutor_url'] = '{}tutors/{}'.format(request.url_root, res['tutor_id'])
    return jsonify(res)

@app.route('/courses/<name>')
def courseByName(name):
    res = []
    for row in Course.query.filter_by(name=name).join(Person, Person.id==Course.tutor_id).add_columns(Person.lastname, Person.firstname):
        lastname, firstname = row.lastname, row.firstname
        row = row.Course.to_dict()
        row['tutor_name'] = '{} {}'.format(firstname, lastname)
        row['tutor_url'] = '{}tutors/{}'.format(request.url_root, row['tutor_id'])
        res.append(row)
    return jsonify(res)

@app.route('/classes/')
def classes():
    try:
        args = request.args
        res = Class.query.filter_by(**args)
        res = list(row.to_dict() for row in res)
        return jsonify(res)
    except Exception:
        raise InvalidUsage('Invalid query string', status_code=410)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
