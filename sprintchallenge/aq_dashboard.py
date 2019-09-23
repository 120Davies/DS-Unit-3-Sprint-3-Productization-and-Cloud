from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from .models import DB
from decouple import config
import openaq


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(APP)
db.init_app(APP)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(25))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '< Time {} -- Value {} >'.format(self.datetime, self.value)

def merge(list1, list2):

    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

def get_datetime_values(city, parameter):
    api = openaq.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)
    if status == 200:
        utc_datetimes = [result['date']['utc'] for result in body['results']]
        values = [result['value'] for result in body['results']]
        tuples = merge(utc_datetimes, values)
        return tuples

@APP.route('/')
def schtml():
    records = Record.query.filter(Record.value>=10).all()
    return render_template('schtml.html', records=records)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    db.drop_all()
    db.create_all()
    for time_value in get_datetime_values('Los Angeles', 'pm25'):
        record = Record(datetime=str(time_value[0]), value=time_value[1])
        db.session.add(record)
    db.session.commit()
    return render_template('refresh.html')

if __name__ == "__main__":
	APP.run(port=9000, debug = True)
