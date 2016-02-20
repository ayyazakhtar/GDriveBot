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
def get_auth_offcloud(username, password):
	session = requests.Session()
	url="https://offcloud.com/api/login/classic"
	data = {"username": username, "password": password}
	response = session.get(url, data=data)		
	return  session.cookies.get_dict()

def get_remote_account_list():
	cookie = get_auth_offcloud(offcloud_user_name, offcloud_password)
	url = 'https://offcloud.com/api/remote-account/list'
	data = {}
	response = requests.get(url,data=data,cookies=cookie)
	if response.status_code == 200:
		return(json.loads(response.text))
	else:
		return None
	

def check_status(ref_no):
	return "downloading"
	
if __name__ == '__main__':
	offcloud_auth_cookie  = get_auth_offcloud('mraqkhan@icloud.com', 'Pakland990')	
	
	url = 'https://offcloud.com/api/remote-account/list'	
	data = {}
	print offcloud_auth_cookie
	response = requests.get(url,data=data,cookies=offcloud_auth_cookie)
	# import pdb; pdb.set_trace()	
		
	print response.status_code
	account_info =  json.loads(response.text)	
	pprint(account_info)
	print type(account_info)
	exit();
		# # {
		# #   "accountId": "5686edea098580b372000527",
		# #   "remoteOptionId": "5686edea098580b372000527",
		# #   "type": "gdrive",
		# #   "username": "14mseeakhan@seecs.edu.pk"
		# # },

	# # url = 'https://offcloud.com/api/remote/status/'
	# # url = 'https://offcloud.com/api/remote/download'
	# # for account in account_info["data"]:
	# if True:
		# print "-------------------------------------------------"
		# # print account['username']
		# # data = {"url" :"magnet:?xt=urn:btih:4B51C4107B41178F60BA6F6411C6A85CA6BA38DC&dn=magic+mike+xxl+2015+1080p+brrip+x264+yify&tr=udp%3A%2F%2Ftracker.publicbt.com%2Fannounce&tr=udp%3A%2F%2Fglotorrents.pw%3A6969%2Fannounce" ,"remoteOptionId": '568906c082747ad611000091'}
				# # 568906c082747ad611000091
				# # ,"requestId": account['remoteOptionId']}
		# print requests.post(url,data=data,cookies=session.cookies.get_dict()).text


	# get_auth_offcloud();
	# get_remote_account_list();
