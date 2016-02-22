from bs4 import BeautifulSoup
import urllib2, codecs
from datetime import date
import datetime
import os
import requests
from pprint import pprint
import json


############################## ------------ OFFCLoud -------------####################################

offcloud_user_name =  'mraqkhan@icloud.com'
offcloud_password = 'Pakland990'
offcloud_auth_cookie= ''
my_user_name = '13mseeaakhtar@seecs.edu.pk'
my_account = {}

# this has to be set before
def auth_offcloud(username, password):
	global offcloud_auth_cookie
	session = requests.Session()
	url="https://offcloud.com/api/login/classic"
	data = {"username": username, "password": password}
	response = session.get(url, data=data)		
	offcloud_auth_cookie = session.cookies.get_dict()
########################### get_remote_account_list ################################
''' Returns the total remote account authorized with offcloud
'''
def get_remote_account_list():	
	url = "https://offcloud.com/api/remote-account/list"
	data = {}
	response = requests.get(url,data=data,cookies=offcloud_auth_cookie)
	if response.status_code == 200:
		return(json.loads(response.text))
	else:
		return None
###############################################################################		

########################### add_remote_download ################################
''' A Dictionary of the following structure is returned
{  "requestId": "",
  "site": "",
  "status": "",
  "originalLink": "",
  "createdOn": ""
}'''
def add_remote_download(down_link):
	url = "https://offcloud.com/api/remote/download"
	data = {"url" :down_link ,"remoteOptionId": my_account['remoteOptionId']}
	response = requests.post(url,data=data,cookies=offcloud_auth_cookie)
	
	if response.status_code == 200:
		return(json.loads(response.text))
	else:
		return None
###############################################################################

		
def init():
	global my_account
	account_info =get_remote_account_list()	
	for account in account_info['data']:
		if account['username'] == my_user_name:
			my_account = account
	
	
########################### check_status ################################
''' A Dictionary of the following structure is returned
{ "status": {
    "status": "",
    "amount": ,
    "requestId": "",
    "fileSize": ,
    "downloadingSpeed": "",
    "downloadingTime": ,
    "fileName": ""
  }	
} '''

def check_status(requestId ):
	url = "https://offcloud.com/api/remote/status"
	data = {"requestId" :requestId }
	response = requests.post(url,data=data,cookies=offcloud_auth_cookie)
	print response
	print response.text
	if response.status_code == 200:
		return(json.loads(response.text))
	else:
		return None
###############################################################################
	

status_msgs = ["created", "downloading", "downloaded"]

if __name__ == '__main__':
	auth_offcloud(offcloud_user_name, offcloud_password)
	init()
	# down_data = add_remote_download(magnet)
	# check_status(down_data['requestId'])
	check_status('56cb0a4a4ff06a5c740000b6')

	exit()
