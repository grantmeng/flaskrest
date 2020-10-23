from flask import Flask
from flask_simpleldap import LDAP

app = Flask(__name__)
# Main
app.config['LDAP_HOST'] = 'ldaps.example.org'
app.config['LDAP_BASE_DN'] = 'ou=Users,o=23972934oihsdfsomekeywoohoo,dc=example,dc=com'
app.config['LDAP_USERNAME'] = 'uid=ldapbinduser,ou=Users,o=4839cxvc678cv8676we87somekeywoohoo,dc=example,dc=com'
app.config['LDAP_PASSWORD'] = 'password'
# ssl
LDAP_SCHEMA = environ.get('LDAP_SCHEMA', 'ldaps')
LDAP_PORT = environ.get('LDAP_PORT', 636)
# openLDAP 
app.config['LDAP_OPENLDAP'] = True
# Users
app.config['LDAP_USER_OBJECT_FILTER'] = '(uid=%s)'
# Groups
app.config['LDAP_GROUP_MEMBER_FILTER'] = '(|(&(objectClass=*)(member=%s)))'
app.config['LDAP_GROUP_MEMBER_FILTER_FIELD'] = 'cn'
# Error Route
# @app.route('/unauthorized') <- corresponds with the path of this route when authentication fails
app.config['LDAP_LOGIN_VIEW'] = 'unauthorized' 
ldap = LDAP(app)
@app.errorhandler(401)
@app.route('/unauthorized')
def unauthorized_message():
    return 'Unauthorized, username or password incorrect'


### Basic Auth
from flask import Flask, g
from flask_simpleldap import LDAP

app = Flask(__name__)
#app.config['LDAP_HOST'] = 'ldap.example.org'  # defaults to localhost
app.config['LDAP_BASE_DN'] = 'OU=users,dc=example,dc=org'
app.config['LDAP_USERNAME'] = 'CN=user,OU=Users,DC=example,DC=org'
app.config['LDAP_PASSWORD'] = 'password'

ldap = LDAP(app)

@app.route('/')
@ldap.basic_auth_required
def index():
    return 'Welcome, {0}!'.format(g.ldap_username)

if __name__ == '__main__':
    app.run()


### Group Auth
import ldap as l
from flask import Flask, g, request, session, redirect, url_for
from flask_simpleldap import LDAP

app = Flask(__name__)
app.secret_key = 'dev key'
app.debug = True

app.config['LDAP_HOST'] = 'ldap.example.org'
app.config['LDAP_BASE_DN'] = 'OU=users,dc=example,dc=org'
app.config['LDAP_USERNAME'] = 'CN=user,OU=Users,DC=example,DC=org'
app.config['LDAP_PASSWORD'] = 'password'
app.config['LDAP_CUSTOM_OPTIONS'] = {l.OPT_REFERRALS: 0}

ldap = LDAP(app)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        # This is where you'd query your database to get the user info.
        g.user = {}
        # Create a global with the LDAP groups the user is a member of.
        g.ldap_groups = ldap.get_user_groups(user=session['user_id'])


@app.route('/')
@ldap.login_required
def index():
    return 'Successfully logged in!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = request.form['user']
        passwd = request.form['passwd']
        test = ldap.bind_user(user, passwd)
        if test is None or passwd == '':
            return 'Invalid credentials'
        else:
            session['user_id'] = request.form['user']
            return redirect('/')
    return """<form action="" method="post">
                user: <input name="user"><br>
                password:<input type="password" name="passwd"><br>
                <input type="submit" value="Submit"></form>"""


@app.route('/group')
@ldap.group_required(groups=['Web Developers', 'QA'])
def group():
    return 'Group restricted page'


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
