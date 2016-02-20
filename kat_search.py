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
# x = "https://kat.cr/usearch/DC'sLegends of tomorrow S01E01 category%3Atv/?field=seeders&sorder=desc"s

def get_tv_show_episode(show_name, season, episode):
	if(season < 10):
		ep_string = "S0" + str(season)
	else:
		ep_string =  "S" + str(season)

	if(episode < 10):	
		ep_string = ep_string  + "E0" + str(episode)
	else:
		ep_string = ep_string  + "E" + str(episode)		

	torrent = get_magnet_link([show_name, ep_string], "tv")
	
	if torrent == None:
		print("Episdoe not found")
		return None;
	else:
		return torrent
	# print "name : " + torrent['name']
	# print "size : " + torrent['size']
	# print "seeders: " + torrent['seeders']
	# print  "magnet Link : " + torrent['magnet']

def search_keyword_in_name(name, keywords):
	match = True
	name = name.lower()		
	name = name.split(' ')
	
	for keyword in keywords:		
		search_res = [s for s in name if keyword.lower() == s]
		if search_res == []:
			match = False
			
	return match


def get_magnet_link(search_list, category):
	# print "----------------------------------------------------------------"
	url = url_base + "usearch/" + ' '.join(search_list) + " category%3A" + category +  "/?field=seeders&sorder=desc"
	response = requests.get(url, verify= True)
	soup = BeautifulSoup(response.text,"html.parser")
	table = soup.find("table", {"class": "data"})
	torrent = {"name":"", "magnet":"", "size":0, "seeders":0}
	if table == None:
		print("page search error")
		return None
	
	for row in table.findAll('tr')[1:]:
		cur_struct = row.findAll('td')			
		name = cur_struct[0].find(attrs={"class" : "cellMainLink"}).getText()		
		matched = search_keyword_in_name(name, search_list)
		
		if matched:
			torrent['name'] = name
			torrent['magnet'] = cur_struct[0].find(attrs={"title" : "Torrent magnet link"})['href']
			torrent['size'] = cur_struct[1].getText()
			torrent['seeders']= cur_struct[4].getText()				
			return torrent
			break
					
	return None;