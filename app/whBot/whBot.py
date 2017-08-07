import json
import sys
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

		raw = requests.get('http://www.wikihow.com/api.php?action=query&list=search&srlimit=25&format=json&srsearch='+args['text'])
		parsed = json.loads(raw.text)
		for attempt in range(0,5):
			try:
				title = random.choice(parsed['query']['search'])
			except:
				response.text = response.text + str(parsed)
				return response.__dict__
			raw = requests.get('http://www.wikihow.com/api.php?action=query&prop=images&format=json&titles='+title['title'])
			parsed = json.loads(raw.text)
			pages = parsed['query']['pages']
			try:
				image = random.choice(pages[list(pages.keys())[0]]['images'])
				break
			except:
				response.text = response.text + "broke at 2\n"
				response.text = response.text + str(pages)
			if attempt == 4:
				return response.__dict__
		raw = requests.get('http://www.wikihow.com/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles='+image['title'])
		parsed = json.loads(raw.text)
		pages = parsed['query']['pages']
		try:
			page = pages[next(iter(pages))]
			info = page['imageinfo'][0]
			url = info['url']
		except:
			response.text = str(page['imageinfo'])
			return response.__dict__
		response.text = "<"+url+"|"+title['title']+">"
		response.response_type = "in_channel"
		return response.__dict__
