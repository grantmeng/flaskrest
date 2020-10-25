#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from dataclasses_json import dataclass_json

db = SQLAlchemy()

@dataclass_json
@dataclass
class Authuser(db.Model):
    id: int
    username: str
    password: str

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

@dataclass_json
@dataclass
class Person(db.Model):
    id: int
    firstname: str
    lastname: str
    gender: str
    age: int

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    gender = Column(String(1))
    age = Column(Integer)

@dataclass_json
@dataclass
class Tutor(db.Model):
    id: int
    info: Person
    courses: 'Course'

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    info = relationship(Person)
    courses = relationship('Course', back_populates='tutor')

@dataclass_json
@dataclass
class Student(db.Model):
    id: int
    info: Person

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    info = relationship(Person)

@dataclass_json
@dataclass
class Course(db.Model):
    id: int
    name: str
    tutor_id: int

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tutor_id = Column(Integer, ForeignKey('tutor.id'), nullable=False)
    tutor = relationship(Tutor, back_populates='courses')

@dataclass_json
@dataclass
class Class(db.Model):
    course: Course
    student: Student

    __tablename__ = 'classes'
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True, nullable=False)
    course = relationship(Course)
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True, nullable=False)
    student = relationship(Student)
