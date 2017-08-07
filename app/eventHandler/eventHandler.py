import os,sys,inspect
import pickle
import json
import requests
import random
import sqlite3
from flask_restful import reqparse, Resource, Api

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from slackFunctions.slackFunctions import *
import config

parser = reqparse.RequestParser()
parser.add_argument('challenge')
parser.add_argument('event')

class slackResponse:
	def __init__(self):
		self.text = ""
		self.type = ""
		self.channel=""
		self.id = 1
		self.response_type = ""
		self.attachments = []

def recordReaction(reaction):
	reactionCounts = {}
	try:
		reactionCounts = pickle.load(open("reactions.p","rb"))
        except:
		pass
	if reaction in reactionCounts:
		reactionCounts[reaction] = reactionCounts[reaction]+1
	else:
		reactionCounts[reaction] = 1
	pickle.dump(reactionCounts, open("reactions.p","wb"))

class eventHandler(Resource):
	def post(self):
		args = parser.parse_args()
		if args['challenge']:
			return args['challenge']
		if args["event"]:
			json_safe = args['event'].replace("u'","\"")
			json_safe = json_safe.replace("'","\"")
			event = json.loads(json_safe)
			item = event["item"]
			recordReaction(event["reaction"])
			#-->BASIC DELETER
			if event["reaction"] == 'thad':
				if isUserAdmin(event["user"]):
					deleteMessage(event["item"])
			#<--BASIC DELETER
			
			#-->MASS DELETE
			elif event["reaction"] == "deletestart":
				if not isUserAdmin(event["user"]):
					return
				conn = sqlite3.connect('data.db')
				cur = conn.cursor()
				cur.execute("SELECT * FROM ranges WHERE channel = '%s'" % item["channel"])
				record = cur.fetchone()
				if record == None:
					cur.execute("INSERT INTO ranges values(?,'',?)",[item["channel"],item["ts"]])
				elif record[2] == '':
					cur.execute("UPDATE ranges set 'oldest' = ? WHERE 'channel' == ?",[item["ts"],item["channel"]])
				elif record[2] != '':
					messageChannel(channelID = item["channel"], message = "Already have a start point")
				if record != None and record[1] != '':
					messages = getMessagesInRange(item["channel"],record[1],item["ts"])
					for mess in messages:
						deleteTimestamp(item["channel"],mess["ts"])
					con.commit()
					cur.execute("DELETE FROM ranges")
					messageChannel(item["channel"],"someone deleted "+str(len(messages))+" messages")

				conn.commit()
				conn.close()
				return
			elif event["reaction"] == "deleteend":
				if not isUserAdmin(event["user"]):
					return
				conn = sqlite3.connect('data.db')
				cur = conn.cursor()
				cur.execute("SELECT * FROM ranges WHERE channel = '%s'" % item["channel"])
				record = cur.fetchone()
				if record == None:
					cur.execute("INSERT INTO ranges values(?,?,'')",[item["channel"],item["ts"]])
				elif record[1] == '':
					cur.execute("UPDATE ranges set 'latest' = ? WHERE 'channel' == ?",[item["ts"],item["channel"]])
				elif record[1] != '':
					messageChannel(channelID = item["channel"], message = "Already have an end point")
				if record != None and record[2] != '':
					messages = getMessagesInRange(item["channel"],item["ts"],record[2])
					for mess in messages:
						deleteTimestamp(item["channel"],mess["ts"])
					conn.commit()
					cur.execute("DELETE FROM ranges")
					messageChannel(item["channel"],"someone deleted "+str(len(messages))+" messages")
				conn.commit()
				conn.close()
				return
			#<--MASS DELETE
			

			elif event["reaction"] == "cop":
				if isUserAdmin(event["user"]):
					message = getMessageByID(channelID = event["item"]["channel"], messageID = event["item"]["ts"])

					toSend = slackRequest()
					toSend.ts = event["item"]["ts"]
					toSend.channel = event["item"]["channel"]
					toSend.text = message["text"] + "\n" + "```user was banned for this comment```" 
					toSend.as_user = False
					response = requests.post('https://slack.com/api/chat.update', data = toSend.__dict__)

					removeReaction(channelID=event["item"]["channel"],messageID=event["item"]["ts"],reaction="cop")
				with open('dump','a') as f:
					f.write(str(message))
					f.write('\n')	
