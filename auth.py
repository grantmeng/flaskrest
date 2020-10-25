#!/usr/bin/python3

from models import Authuser

# get run when a post is made to /auth with application/json as a content type
def authenticate(username, password):
    authuser = Authuser.query.filter(Authuser.username == username).first()
    if authuser.password == password: return authuser
# get run when jwt_required
def identity(payload):
    user_id = payload['identity']
    return Authuser.query.get_or_404(user_id)

# generate token
# token = curl http://localhost:5000/auth -d '{"username": "grant", "password": "grant"}' --header "Content-Type: application/json"
# curl http://localhost:5000/persons/ -H "Authorization: JWT token"
