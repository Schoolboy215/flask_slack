import json
import requests
import random
from flask_restful import reqparse, Resource, Api

parser = reqparse.RequestParser()
parser.add_argument('text', type=str, help='slack command text')

class slackResponse:
	def __init__(self):
		self.text = ""
		self.response_type = ""
		self.attachments = []

class urbanBot(Resource):
	def get(self):
		args = parser.parse_args()
		response = slackResponse()
		response.text = "Word not found"

		raw = requests.get('http://api.urbandictionary.com/v0/define?term='+args['text'])
		parsed = json.loads(raw.text)
		try:
			picked = random.choice(parsed['list'])
		except:	
			return response.__dict__
		response.text = "*"+picked['word']+"* :  "
		response.text = response.text + picked['definition']
		response.attachments.append({'text':picked['example']})
		response.response_type = "in_channel"
		return response.__dict__
