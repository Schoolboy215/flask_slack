from flask import Flask
from flask_restful import reqparse, Resource, Api
from urbanBot.urbanBot import urbanBot
from whBot.whBot import whBot
from eventHandler.eventHandler import eventHandler
from reactionCounts.reactionCounts import reactionCounts

app = Flask(__name__)
api = Api(app)

api.add_resource(urbanBot, '/define')
api.add_resource(whBot, '/wikiHow')
api.add_resource(eventHandler, '/events')
api.add_resource(reactionCounts, '/reactionCounts')

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
