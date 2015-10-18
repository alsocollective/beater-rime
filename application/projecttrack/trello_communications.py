import requests

from django.conf import settings

# from projecttrack import models as ptrack

print "\n\n"


def make_board(name):
	url = "https://api.trello.com/1/boards/?key=%s&token=%s"%(settings.TRELLO_API["key"],settings.TRELLO_API["token"])
	data = {
		"name":name
	}
	r = requests.post(url,json=data)
	if r.status_code != 200:
		print "\n\n%s\n\n"%r.text
		return {"id":"","shortUrl":""}
	return r.json() 


def make_list(name,board):
	url = "https://api.trello.com/1/lists/?key=%s&token=%s"%(settings.TRELLO_API["key"],settings.TRELLO_API["token"])
	data = {
		"name":name,
		"idBoard":board
	}
	r = requests.post(url,json=data)
	return r.json() 

def make_card(name,trello_list,due):
	url = "https://api.trello.com/1/cards/?key=%s&token=%s"%(settings.TRELLO_API["key"],settings.TRELLO_API["token"])

	data = {
		"name":name,
		"idList":trello_list,
		"due":due.ctime()
	}
	r = requests.post(url,json=data)
	print r.text
	return r.json() 

def update_card(name,trello_card,trello_list,due):
	url = "https://api.trello.com/1/cards/%s?key=%s&token=%s"%(trello_card,settings.TRELLO_API["key"],settings.TRELLO_API["token"])
	data = {
		"name":name,
		"due":due.ctime()
	}
	r = requests.put(url,json=data)
	print r.text
	return r.json()	

# id #5623166d6e74bf839e4164be
# short url = "https://trello.com/b/pxByCfXZ"


# board = make_board("bohdan first api board")
board = {"id":"5623166d6e74bf839e4164be","name":"bohdan first api board","desc":"","descData":None,"closed":False,"idOrganization":None,"pinned":False,"url":"https://trello.com/b/pxByCfXZ/bohdan-first-api-board","shortUrl":"https://trello.com/b/pxByCfXZ","prefs":{"permissionLevel":"private","voting":"disabled","comments":"members","invitations":"members","selfJoin":True,"cardCovers":True,"cardAging":"regular","calendarFeedEnabled":False,"background":"blue","backgroundColor":"#0079BF","backgroundImage":None,"backgroundImageScaled":None,"backgroundTile":False,"backgroundBrightness":"unknown","canBePublic":True,"canBeOrg":True,"canBePrivate":True,"canInvite":True},"labelNames":{"green":"","yellow":"","orange":"","red":"","purple":"","blue":"","sky":"","lime":"","pink":"","black":""}}

# trello_list = make_list("first",board)
trello_list = {"id":"56231c4b5c44b41f796b54f1","name":"first","closed":False,"idBoard":"5623166d6e74bf839e4164be","pos":8192}

# trello_card = make_card("first card",trello_list)
trello_card = {"id":"56231d1e6832786131665b71","badges":{"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"comments":0,"attachments":0,"description":False,"due":None},"checkItemStates":[],"closed":False,"dateLastActivity":"2015-10-18T04:16:30.455Z","desc":"","descData":{"emoji":{}},"due":None,"email":"bohdan_cooler_than_you+556e023f9b80bbbd844708a7+56231d1e6832786131665b71+da9774d05c3a34db8f6537d22acaa5c4057105e6@boards.trello.com","idBoard":"5623166d6e74bf839e4164be","idChecklists":[],"idLabels":[],"idList":"56231c4b5c44b41f796b54f1","idMembers":[],"idShort":1,"idAttachmentCover":None,"manualCoverAttachment":False,"labels":[],"name":"first card","pos":16384,"shortUrl":"https://trello.com/c/1BUqe2tM","url":"https://trello.com/c/1BUqe2tM/1-first-card","stickers":[]}




print "\n\n"
