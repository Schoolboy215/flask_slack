import json
import requests
import random
from flask_restful import reqparse, Resource, Api
import config

class slackResponse:
	def __init__(self):
		self.text = ""
		self.type = ""
		self.channel=""
		self.id = 1
		self.response_type = ""
		self.attachments = []

class slackRequest:
	def __init__(self):
		self.ok = True
		self.token = config.token

def pingChannel(channelID):
	sendBack = slackRequest()
	sendBack.channel = channelID
	sendBack.text = "You reached a breakpoint"
	
	requests.post('https://slack.com/api/chat.postMessage', data=sendBack.__dict__)

def messageChannel(channelID, message):
	sendBack = slackRequest()
	sendBack.channel = channelID
	sendBack.text = message
	
	requests.post('https://slack.com/api/chat.postMessage', data=sendBack.__dict__)

def isUserAdmin(userId):
	sendBack = slackRequest()
	sendBack.user = userId
	response = requests.post('https://slack.com/api/users.info', data=sendBack.__dict__)
	parsed = json.loads(response._content)
	user = parsed["user"]
	return user["is_admin"]

def getMessageByID(channelID, messageID):
	sendBack = slackRequest()
	sendBack.channel = channelID
	sendBack.latest = messageID
	sendBack.oldest = messageID
	sendBack.inclusive = True
	
	response = requests.post('https://slack.com/api/channels.history', data=sendBack.__dict__)
	parsed = json.loads(response._content)
	return parsed["messages"][0]

def getMessagesInRange(channelID, latestTS, oldestTS):
	sendBack = slackRequest()
	sendBack.channel = channelID
	sendBack.latest = latestTS
	sendBack.oldest = oldestTS
	sendBack.inclusive = True

	response = requests.post('https://slack.com/api/channels.history', data=sendBack.__dict__)
	parsed = json.loads(response._content)
	toReturn = parsed["messages"]
	with open('dump','a') as f:
                f.write(str(toReturn))
                f.write('\n')
	return toReturn

def removeReaction(channelID, messageID, reaction):
	sendBack = slackRequest()
	sendBack.channel = channelID
	sendBack.timestamp = messageID
	sendBack.name = reaction

	requests.post('https://slack.com/api/reactions.remove', data=sendBack.__dict__)

def deleteMessage(item):
	sendBack = slackRequest()
	sendBack.ts = item["ts"]
	sendBack.channel = item["channel"]
	requests.post('https://slack.com/api/chat.delete',data=sendBack.__dict__)

def deleteTimestamp(channel,timestamp):
	sendBack = slackRequest()
	sendBack.ts = timestamp
	sendBack.channel = channel
	requests.post('https://slack.com/api/chat.delete',data=sendBack.__dict__)
