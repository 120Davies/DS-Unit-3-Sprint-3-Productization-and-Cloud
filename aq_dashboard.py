from flask import Flask

APP = Flask(__name__)


@APP.route('/')
def root():
    return '''<html><head><title>Hello!</title></head><body><hl></body></html>'''
    return 'TODO - part 2 and beyond!' 