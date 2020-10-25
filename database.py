#!/usr/bin/python3

from config import *
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

engine = create_engine(DB_URI, echo=True)
meta = MetaData()
meta.reflect(bind=engine) # key to get all tables
authuser = meta.tables.get('authuser')
person = meta.tables.get('person')
tutor = meta.tables.get('tutor')
student = meta.tables.get('student')
course = meta.tables.get('course')
classes = meta.tables.get('classes')

def create_tables():
    global authuser
    if authuser == None:
        authuser = Table(
           'authuser', meta, 
           Column('id', Integer, primary_key=True), 
           Column('username', String), 
           Column('password', String))
    global person
    if person == None:
        peron = Table(
           'person', meta, 
           Column('id', Integer, primary_key=True), 
           Column('firstname', String), 
           Column('lastname', String),
           Column('gender', String(1)),
           Column('age', Integer))
    global tutor
    if tutor == None:
        tutor = Table(
           'tutor', meta, 
           Column('id', Integer, ForeignKey('person.id'), primary_key=True))
    global student
    if student == None:
        student = Table(
           'student', meta, 
           Column('id', Integer, ForeignKey('person.id'), primary_key=True))
    global course
    if course == None:
        course = Table(
           'course', meta, 
           Column('id', Integer, primary_key=True), 
           Column('name', String), 
           Column('tutor_id', Integer, ForeignKey('tutor.id'), nullable=False))
    global classes
    if classes == None:
        classes = Table(
            'classes', meta, 
            Column('course_id', Integer, ForeignKey('course.id'), primary_key=True, nullable=False),
            Column('student_id', Integer, ForeignKey('student.id'), primary_key=True, nullable=False))
    meta.create_all(engine)

def insert_tables():
    conn = engine.connect()
    authuser = meta.tables.get('authuser')
    conn.execute(authuser.insert(), [
        {'username': 'bear', 'password': 'bear'},
        {'username': 'grant', 'password': 'grant'}])
    person = meta.tables.get('person')
    conn.execute(person.insert(), [
        {'firstname': 'Grant', 'lastname': 'Meng', 'gender': 'M', 'age': 46},
        {'firstname': 'Rain', 'lastname': 'Cao', 'gender': 'F', 'age': 40},
        {'firstname': 'Dan', 'lastname': 'Wu', 'gender': 'M', 'age': 14},
        {'firstname': 'Mike', 'lastname': 'Meng', 'gender': 'M', 'age': 12},
        {'firstname': 'Bear', 'lastname': 'Meng', 'gender': 'F', 'age': 20}])
    tutor = meta.tables.get('tutor')
    conn.execute(tutor.insert(), [
        {'id': 1},
        {'id': 2}])
    student = meta.tables.get('student')
    conn.execute(student.insert(), [
        {'id': 3},
        {'id': 4}])
    course = meta.tables.get('course')
    conn.execute(course.insert(), [
        {'name': 'Math', 'tutor_id': 1},
        {'name': 'Math', 'tutor_id': 2},
        {'name': 'ELA', 'tutor_id': 2},
        {'name': 'Science', 'tutor_id': 1},
        {'name': 'Social Study', 'tutor_id': 2}])
    classes = meta.tables.get('classes')
    conn.execute(classes.insert(), [
        {'course_id': 1, 'student_id': 3},
        {'course_id': 1, 'student_id': 4},
        {'course_id': 2, 'student_id': 3},
        {'course_id': 2, 'student_id': 4},
        {'course_id': 3, 'student_id': 3},
        {'course_id': 3, 'student_id': 4},
        {'course_id': 4, 'student_id': 3},
        {'course_id': 4, 'student_id': 4}])

def drop_tables():
    tables = []
    for table in (authuser, person, course, tutor, student, classes):
        if table != None: tables.append(table)
    meta.drop_all(engine, tables=tables)

if __name__ == '__main__':
    drop_tables()
    create_tables()
    insert_tables()
