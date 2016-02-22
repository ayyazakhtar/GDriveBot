from pytvdbapi import api
import sys
import json
import os
import fnmatch
import offcloud_api
import kat_search
import sqlite3 as lite
from datetime import date
from datetime import datetime
from pprint import pprint



offcloud_user_name =  'mraqkhan@icloud.com'
offcloud_password = 'Pakland990'

def get_new_show_input(db_directory):
	db = api.TVDB("B43FF87DE395DF56")

	if not os.path.exists(db_directory):
		print "tv shows directory does not exist"
		os.makedirs(db_directory)
	while True:
		print("--------------------------------------")
		name = raw_input("Enter TV Show name?  :  ")
		results = db.search(name, "en")
		print "Search Results :"
		count = 1
		for result in results:
			print( str(count)+ " - " + result.SeriesName)
			count = count + 1
		print (str(count) + " - Search Again")
		sel = raw_input("Select 1 - " + str(count) + " : ")
		if (int(sel) == count):
			continue
		else :
			show = results[int(sel)- 1]			
		print("Selected Series : " + show.SeriesName)		
		show_data = {'title':show.SeriesName, 'imdb_id':show.IMDB_ID, 'seasons': [], "erred_episodes" : []}
		json.dump(show_data, open(db_directory +show.SeriesName.replace(' ', '_')+ ".json", 'w'))
		break
	
def initialize_tables(cur):	
	cur.execute("DROP TABLE IF EXISTS item")	
	cur.execute("CREATE TABLE IF NOT EXISTS item( imdb_id TEXT, title TEXT, type TEXT)")
	
	cur.execute("DROP TABLE IF EXISTS seasons")	
	cur.execute("CREATE TABLE IF NOT EXISTS seasons(show_title TEXT, season_number INT, status TEXT)")
	
	cur.execute("DROP TABLE IF EXISTS seasons")	
	cur.execute("CREATE TABLE IF NOT EXISTS seasons(show_title TEXT, season_number INT, status TEXT)")
	
	# cur.execute("DROP TABLE IF EXISTS tvshows")	
	# cur.execute("CREATE TABLE IF NOT EXISTS tvshows(show_title TEXT, season INT, episode INT, episode_title TEXT, status TEXT, offcloud_ref_no INT,magnet TEXT)")

	# cur.execute("DROP TABLE IF EXISTS movies")	
	# cur.execute("CREATE TABLE IF NOT EXISTS movies( imdb_id TEXT, movie_title TEXT, status TEXT, offcloud_ref_no INT)")
	cur.execute("INSERT INTO item VALUES(?,?,?)", ("12", "The flash (2014)", "tv show"))
	cur.execute("INSERT INTO item VALUES(?,?,?)", ("13", "Arrow", "tv show"))
	cur.execute("INSERT INTO item VALUES(?,?,?)", ("14", "homeland (2014)", "tv show"))
	cur.execute("INSERT INTO item VALUES(?,?,?)", ("15", "despcable me ", "movie"))
	cur.execute("INSERT INTO item VALUES(?,?,?)", ("16", "despicable me 2 ", "movie"))
	cur.execute("INSERT INTO item VALUES(?,?,?)", ("17", "minions", "movie"))
	
	cur.execute("INSERT INTO seasons VALUES(?,?,?)", ("Arrow", 1, "downloaded"))
	cur.execute("INSERT INTO seasons VALUES(?,?,?)", ("Arrow", 2, "downloaded"))
	cur.execute("INSERT INTO seasons VALUES(?,?,?)", ("Arrow", 3, "downloading"))
	cur.execute("INSERT INTO seasons VALUES(?,?,?)", ("Arrow", 4, "downloading"))
	
	cur.execute("INSERT INTO seasons VALUES(?,?,?)", ("The flash (2014)", 1, "downloading"))
	cur.execute("INSERT INTO seasons VALUES(?,?,?)", ("The flash (2014)", 2, "downloading"))
	
	
def db_storage():
	db_name = "torrent_db"
	con = lite.connect(db_name)

	with con:    
		con.row_factory = lite.Row		
		cur = con.cursor()		
		initialize_tables(cur)		
		cur.execute("PRAGMA table_info(item)")
		cur.execute("PRAGMA table_info(seasons)")
			
		# cur.execute("INSERT INTO Cars VALUES(2,'Audi',52642)")
		
		
		# cur.execute("SELECT * FROM Cars")
		# cur.execute("SELECT * FROM item WHERE imdb_id=? ", ("imdb_id",)) 
		cur.execute("SELECT * FROM item LEFT OUTER JOIN seasons ON item.title = seasons.show_title WHERE type='tv show' AND seasons.	show_title='The flash (2014)'") 
		rows = cur.fetchall()

		for row in rows:
			print row
			print row['show_title']
'''
Episode Info FOrmat
{
"status": "", 
"magnet": "",
"request_id": 
"attempt"
}'''

def get_remote_download(magnet):
	if offcloud_api.offcloud_auth_cookie == '':
		offcloud_api.auth_offcloud(offcloud_user_name, offcloud_password)
	return offcloud_api.add_remote_download(magnet)		

def offcloud_init():
	if offcloud_api.offcloud_auth_cookie == '':
		offcloud_api.auth_offcloud(offcloud_user_name, offcloud_password)
	offcloud_api.init()
		
		
def get_torrent_status(requestId):
	# also add time based token expiry and re authorization
	if offcloud_api.offcloud_auth_cookie == '':
		auth_offcloud(offcloud_user_name, offcloud_password)
	return offcloud_api.check_status(requestId)

def start_episode_download(magnet, attempt):
	down_data = get_remote_download(magnet)		
	episode_data = {}
	episode_data['magnet'] = magnet
	
	if down_data != None:								
		episode_data['status'] = down_data['status']
		episode_data['request_id'] =down_data['requestId']
	else:
		episode_data['status'] = "Error_retry"
		episode_data['request_id'] = 0
	episode_data['attemp'] = attempt + 1	
	return episode_data
	
	
def main(argv):	
	offcloud_init()
	db = api.TVDB("B43FF87DE395DF56")
	cwd = os.path.dirname(os.path.realpath(__file__))
	db_directory = cwd + "/database/tvshows/"

	
	if len(argv) > 1:
		if argv[1] == 'add':		#	Adding new TV shows to download list
			get_new_show_input(db_directory)
			
	file_list = []			
	for file in os.listdir(db_directory):
		if fnmatch.fnmatch(file, '*.json'):
			file_list.append(file)		
			
	print file_list
	for show_file in file_list:
		show_data = json.load(open(db_directory + show_file))	
		show = db.get_series( show_data["imdb_id"], "en" , id_type='imdb', cache=True)
		show.update()		
		print '-------------------' + str(show.SeriesName) + ' ------------------------'

		for season in show:
			season_no = season.season_number - 1
				
			if season.season_number == 0:
				continue
			print 'Season : ' + str(season.season_number) 
				
			if (len(show_data['seasons']) < (season.season_number)):
				show_data['seasons'].append([])	
				
			for episode in season:	
				print '\tEpisode : ' + str(episode.EpisodeNumber)
				episode_no = episode.EpisodeNumber - 1
				today = (date.today()).toordinal()
				ep_date = (episode.FirstAired).toordinal()
				if ep_date < today + 1 : 				# +1 to download episodes that are atleast a day old.
												
					if (len(show_data['seasons'][season_no]) < (episode.EpisodeNumber)):
						show_data['seasons'][season_no].append({})
					
					if show_data['seasons'][season_no][episode_no] == {}:
						episode_torrent = kat_search.get_tv_show_episode(show.SeriesName, season.season_number, episode.EpisodeNumber)						
						
						if episode_torrent == None:							
							show_data['seasons'][season_no][episode_no] = { 'magnet' : "", 'status' : "ERROR_no_magnet",'request_id' : 0, 'attempt' : 1}
							print("ERROR_no_magnet")
						else:							
							show_data['seasons'][season_no][episode_no] = start_episode_download(episode_torrent['magnet'], 0)
							# print(show_data['seasons'][season_no][episode_no]["status"])
						
							
					else:			
						cur_episode  = show_data['seasons'][season_no][episode_no];
						
						if cur_episode['status'] == "Error_retry":
							if cur_episode["attempt"] <= 5:
								show_data['seasons'][season_no][episode_no] = start_episode_download(cur_episode['magnet'], cur_episode["attempt"])							
							else:
								show_data['seasons'][season_no][episode_no] = { 'magnet' : "", 'status' : "ERROR_retry_failed",'request_id' : 0, 'attempt' : 5}
						else:
							if (cur_episode['status']!= "downloaded" ) or (cur_episode['status'] != "ERROR_no_magnet") or (cur_episode['status'] != "ERROR_retry_failed"):					
								off_cloud_status = get_torrent_status(cur_episode['request_id'])													
								if off_cloud_status['status']['status'] == "downloaded":

									show_data['seasons'][season_no][episode_no]['status'] = off_cloud_status['status']['status']
									# write code to push the directory structure to google sheets that will be used to organize the files							
			json.dump(show_data, open(db_directory + show_file, 'w'))
			exit()
		json.dump(show_data, open(db_directory + show_file, 'w'))

if __name__ == '__main__':
	main(sys.argv)