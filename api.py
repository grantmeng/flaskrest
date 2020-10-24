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

@app.route('/persons/', methods=['GET', 'POST'])
def persons():
    if request.method == 'GET':
        try:
            app.logger.info('Getting person list')
            args = dict(request.args)
            page = per_page = None
            if 'page' in args: page = int(args.pop('page'))
            if 'per_page' in args: per_page = int(args.pop('per_page'))
            res = []
            for row in Person.query.filter_by(**args).paginate(page, per_page, False).items:
                row = row.to_dict()
                row['role'] = ''
                if Student.query.get(row['id']): row['role'] = 'Student'
                if Tutor.query.get(row['id']): row['role'] = 'Tutor'
                res.append(row)
            return jsonify(res)
        except Exception as e:
            print(e)
            raise InvalidUsage('Invalid query string', status_code=410, payload={'payload': 'Please check the query string'})
    elif request.method == 'POST': # curl -d "firstname=Dog&lastname=Meng&age=10" -X POST http://localhost:5000/persons/
        dict_data = {
            'lastname': request.form.get('lastname', ''),
            'firstname': request.form.get('firstname', ''),
            'age': request.form.get('age', None),
            'gender': request.form.get('gender', 'M')
        }
        person = Person(**dict_data)
        db.session.add(person)
        db.session.commit()
        dict_data['id'] = person.id
        dict_data['msg'] = 'Person created'
        return jsonify(dict_data)

@app.route('/persons/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def person(id):
    if request.method == 'GET': # curl -X GET http://localhost:5000/persons/1
        res = Person.query.get(id)
        if res:
            res = res.to_dict()
            res['role'] = ''
            if Student.query.get(res['id']): res['role'] = 'Student'
            if Tutor.query.get(res['id']): res['role'] = 'Tutor'
        return jsonify(res)
    elif request.method == 'PUT': # curl -d "firstname=Bear&age=30" -X PUT http://localhost:5000/persons/5
        lastname = request.form.get('lastname', None)
        firstname = request.form.get('firstname', None)
        age = request.form.get('age', None)
        gender = request.form.get('gender', None)
        person = Person.query.get(id)
        if lastname: person.lastname = lastname
        if firstname: person.firstname = firstname
        if age: person.age = age
        if gender: person.gender = gender
        db.session.commit()
        return jsonify(person.to_dict())
    elif request.method == 'DELETE': # curl -X DELETE http://localhost:5000/persons/5
        person = Person.query.get(id)
        db.session.delete(person)
        db.session.commit()
        dict_data = {'id': id, 'msg': 'Person deleted'}
        return jsonify(dict_data)

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
