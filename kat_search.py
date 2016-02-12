from bs4 import BeautifulSoup
import urllib2, codecs
from datetime import date
import datetime
import os
import requests
from pprint import pprint
import json

########################################## ------------ KickAss -------------############################################


url_base= 'https://www.kat.cr/'
x = "https://kat.cr/usearch/DC'sLegends of tomorrow S01E01 category%3Atv/?field=seeders&sorder=desc"
# url_temp= "https://kat.cr/usearch/DC's legends of tomorrow/"

def get_tv_show_episode(show_name, season, episode):
	if(season < 10):
		ep_string = "S0" + str(season)	;
	else:
		ep_string =  "S" + str(season)	;

	if(episode < 10):	
		ep_string = ep_string  + "E0" + str(episode)	;
	else:
		ep_string = ep_string  + "E" + str(episode)	;		

	search_string = show_name + " " + ep_string
	torrent = get_magnet_link(search_string, "tv")
	


	if (((torrent['name'].lower()).find(show_name.lower()) == -1 ) or ((torrent['name'].lower()).find(ep_string.lower()) == -1) ):
		print "episode not found"
	else :
		print "name : " + torrent['name']
		print "size : " + torrent['size']
		print "seeders: " + torrent['seeders']
		print  "magnet Link : " + torrent['magnet']





def get_magnet_link(torrent_name, category):
	print "----------------------------------------------------------------"
	url = url_base + "usearch/" + torrent_name + " category%3A" + category +  "/?field=seeders&sorder=desc"
	print url
	response = requests.get(url, verify= True)
	soup = BeautifulSoup(response.text,"html.parser")
	table = soup.find("table", {"class": "data"})
	torrent = {"name":"", "magnet":"", "size":0, "seeders":0}
	if table == None:
		print("page search error")
		print "----------------------------------------------------------------"
		return torrent
	
	for row in table.findAll('tr')[1:]:
		cur_struct = row.findAll('td')
		
		torrent['name'] = cur_struct[0].find(attrs={"class" : "cellMainLink"}).getText()
		torrent['magnet'] = cur_struct[0].find(attrs={"title" : "Torrent magnet link"})['href']
		torrent['size'] = cur_struct[1].getText()
		torrent['seeders']= cur_struct[4].getText()	
		print "----------------------------------------------------------------"
		return torrent




# for season in range(1,3):
# 	for episode in range(1,5):
# 		get_tv_show_episode("DC's Legends of tomorrow", season, episode);



########################################## ------------ OFFCLoud -------------############################################
# def get_auth_offcloud():
# 	url="https://offcloud.com/api/login/classic"
# 	data = {"username": 'mraqkhan@icloud.com', "password": 'Pakland990'}
# 	print requests.post(url, data=data).text

# def get_remote_account_list():
# 	url = 'https://offcloud.com/api/remote-account/list'
# 	data = {}
# 	print requests.post(url, data=data).text


# session = requests.Session()
# url="https://offcloud.com/api/login/classic"
# data = {"username": 'mraqkhan@icloud.com', "password": 'Pakland990'}
# print session.get(url, data=data).text
# # url = 'https://offcloud.com/api/login/check'

# url = 'https://offcloud.com/api/remote-account/list'	
# data = {}
# account_info =  json.loads(requests.get(url,data=data,cookies=session.cookies.get_dict()).text)

#     # {
#     #   "accountId": "5686edea098580b372000527",
#     #   "remoteOptionId": "5686edea098580b372000527",
#     #   "type": "gdrive",
#     #   "username": "14mseeakhan@seecs.edu.pk"
#     # },

# # url = 'https://offcloud.com/api/remote/status/'
# url = 'https://offcloud.com/api/remote/download'
# # for account in account_info["data"]:
# if True:
# 	print "-------------------------------------------------"
# 	# print account['username']
# 	data = {"url" :"magnet:?xt=urn:btih:4B51C4107B41178F60BA6F6411C6A85CA6BA38DC&dn=magic+mike+xxl+2015+1080p+brrip+x264+yify&tr=udp%3A%2F%2Ftracker.publicbt.com%2Fannounce&tr=udp%3A%2F%2Fglotorrents.pw%3A6969%2Fannounce" ,"remoteOptionId": '568906c082747ad611000091'}
# 			# 568906c082747ad611000091
# 			# ,"requestId": account['remoteOptionId']}
# 	print requests.post(url,data=data,cookies=session.cookies.get_dict()).text


# # get_auth_offcloud();
# # get_remote_account_list();
