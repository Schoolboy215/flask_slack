import json
import pickle
import operator
from flask_restful import reqparse, Resource, Api

parser = reqparse.RequestParser()
parser.add_argument('text', type=str, help='slack command text')

class slackResponse:
	def __init__(self):
		self.text = ""
		self.response_type = ""
		self.attachments = []

class reactionCounts(Resource):
	def get(self):
		counts = pickle.load(open("reactions.p","rb"))
		sorted_counts = sorted(counts.items(), key=operator.itemgetter(0))
		response = slackResponse()
		response.text = "Here are the current reaction counts:\n"
		for reaction in sorted_counts:
			response.text = response.text + ":"+reaction[0]+": : "+str(reaction[1])+"\n" 
		#response.text = json.dumps(sorted_counts)
		return response.__dict__
