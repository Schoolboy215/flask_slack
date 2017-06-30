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

class whBot(Resource):
	def get(self):
		args = parser.parse_args()
		response = slackResponse()
		response.text = "Topic not found"

		raw = requests.get('http://wikihow.com/api.php?action=query&list=allimages&format=json&ailimit=100&aifrom='+args['text'])
		parsed = json.loads(raw.text)
		try:
			picked = random.choice(parsed['query']['allimages'])
		except:	
			return response.__dict__
		response.text = "<"+picked['url']+"|"+args['text']+">"
		response.response_type = "in_channel"
		return response.__dict__
