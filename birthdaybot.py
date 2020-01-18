"""
This script listens for websocket and allows to save/update
the given user's name and date of birth in the SQLite database
and then shows days count until specific username's birthday (or congrats).
Request format is PUT /hello/<username> [a-zA-Z] { "dateOfBirth": "YYYY-MM-DD" }
and GET /hello/<username>.
"""

from flask import Flask, request, json
from datetime import date, datetime
from app import db, app
from app.models import User

day_now = datetime.now().date().day
month_now = datetime.now().date().month

def create_table():
    '''
    create user table is not exist
    '''
    db.create_all()

def check_date(date_str):
    '''
    check if the date is correct and in the past
    '''
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Bad date format, should be YYYY-MM-DD')
    if datetime.strptime(date_str, '%Y-%m-%d') > datetime.now():
        raise ValueError("You can't be born in the future!")
    else:
        return str(date_str)

def user_exists(name):
    '''
    check if user already in the DB
    '''
    qry = User.query.filter_by(name = name)
    if qry.count() > 0:
        return(True)
    else:
        return(False)

def save_to_db(name, b_date):
    '''
    save new user to DB or update if exists
    '''
    create_table()
    if user_exists(name):
        User.query.filter_by(name = name).update({'b_date': b_date})
    else:
        db.session.add(User(name=name, b_date=b_date))
    db.session.commit()

def read_from_db(name):
    '''
    get birth date from DB
    '''
    b_date = User.query.filter_by(name = name).first()
    return(datetime.strptime(str(b_date), '%Y-%m-%d').date())

def get_user_birthday(name):
    '''
    get and return user birthday
    '''
    try:
        b_date = read_from_db(name)
    except ValueError:
        raise ValueError('no such user, please add')
    return b_date

def count_days_to_birthday(name, b_date):
    '''
    count days till birthday
    '''
    if (b_date.month < month_now) or (b_date.month == month_now and b_date.day < day_now):
        b_date = b_date.replace(year=datetime.now().date().year + 1)
        delta = abs(datetime.now().date() - b_date)
        days = f'Hello, {name}! Your birthday is in {int(delta.total_seconds() / 60 /60 /24)} day(s)'
        return days
    else:
        delta = abs(datetime.now().date() - b_date.replace(year=datetime.now().date().year))
        days = f'Hello, {name}! Your birthday is in {int(delta.total_seconds() / 60 /60 /24)} day(s)'
        return days

def make_resp(name):
    '''
    make response to user
    '''
    b_date = get_user_birthday(name)
    if b_date.month == month_now and b_date.day == day_now:
        days = f'Hello, {name}! Happy birthday!'
        return days
    else:
        days = count_days_to_birthday(name, b_date)
        return days

@app.route('/hello/<username>', methods=['GET', 'PUT'])
def hello(username):
    '''
    handle request method
    '''
    result = None
    if request.method == 'PUT':
        result = doPut(request, username)
    elif request.method == 'GET':
        result = doGet(request, username)
    return result

def doPut(request, username):
    '''
    check and save PUT request
    '''
    name = username
    response = ''
    if not request.is_json:
        response = app.response_class(
            response='{"result": "incorrect json"}',
            status=400,
            mimetype='application/json'
        )
    elif not name.isalpha():
        response = app.response_class(
            response='{"result": "incorrect username"}',
            status=400,
            mimetype='application/json'
        )
    else:
        b_date = request.json.get('dateOfBirth', None)
        try:
            resp = check_date(b_date)
        except ValueError as err:
            resp = str(err)
            response = app.response_class(
                response='{"result": "'+resp+'"}',
                status=200,
                mimetype='application/json'
            )
            return response
        save_to_db(name, b_date)
        response = app.response_class(
            status=204,
        )
    return response

def doGet(request, username):
    '''
    send user data on GET request
    '''
    try:
        resp = make_resp(username)
    except ValueError as err:
        resp = str(err)
    response = app.response_class(
        response='{"result": "'+str(resp)+'"}',
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)