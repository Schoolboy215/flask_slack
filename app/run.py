from flask import Flask
from flask_restful import reqparse, Resource, Api
from urbanBot.urbanBot import urbanBot
from eventHandler.eventHandler import eventHandler

app = Flask(__name__)
api = Api(app)

api.add_resource(urbanBot, '/define')
api.add_resource(eventHandler, '/events')

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
