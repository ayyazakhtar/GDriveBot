from pytvdbapi import api
import sys
import json
import os
import fnmatch
import offcloud_api
# import kat_search
#from debug import debug_print
# import debug
import sqlite3 as lite
from datetime import date
from datetime import datetime
from pprint import pprint
import feedparser

# debug.debug_level = 0
mov_downloaded_file = ''
mov_to_down_file  = ''
config_file = "myconfig.json"
# system_state_file = "config.json"
max_active_downloads = ''
cur_active_downloads  = ''
imdb_lists = ["http://rss.imdb.com/user/ur30511277/watchlist", "http://rss.imdb.com/user/ur30511277/ratings"]

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

def start_episode_download(magnet, attempt):
	down_data = offcloud_api.get_remote_download(magnet)		
	print down_data
	episode_data = {}
	episode_data['magnet'] = magnet
	
	if down_data != None:								
		episode_data['status'] = down_data['status']
		episode_data['request_id'] =down_data['requestId']
	else:
		episode_data['status'] = "Error_retry"
		episode_data['request_id'] = 0
	episode_data['attempt'] = attempt + 1	
	return episode_data
		
def add_movie_to_down_list(id):
	cwd = os.path.dirname(os.path.realpath(__file__))
	movie_db_directory = cwd + "/database/movies/"

	movies_downloaded = json.load(open(movie_db_directory + mov_downloaded_file))
	movies_to_download = json.load(open(movie_db_directory + mov_to_down_file))
				
	if (id not in movies_to_download ) and (id not in movies_downloaded):
		print "movie does not exist in list adding"
		movies_to_download.append(id)
		
	json.dump(movies_downloaded, open(movie_db_directory + mov_downloaded_file, 'w'))
	json.dump(movies_to_download, open(movie_db_directory + mov_to_down_file, 'w'))
				
def get_rss_movie_updates():
	for rss_url in imdb_lists:
		data = feedparser.parse(rss_url)				
		for item in data['entries']:
			id = item['id'].split("/")[-2]
			add_movie_to_down_list(id)
	
def main(argv):	
	
	cwd = os.path.dirname(os.path.realpath(__file__))
	system_state = json.load(open(cwd + config_file))
	
	get_rss_movie_updates()
	exit()
	# debug.dbprint("this is sparta mofo : " + str(10), 1);
	offcloud_api.offcloud_init()
	# debug.dbprint("this is sparta mofo : " + str(10), 1);
	db = api.TVDB("B43FF87DE395DF56")
	
	db_directory = cwd + "/database/tvshows/"
	
	if len(argv) > 1:
		print "extra arguements provided"
		if argv[1] == 'add':		#	Adding new TV shows to download list
			get_new_show_input(db_directory)
		else:
			print "invalid arguement passed"
			
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
				# print episode.FirstAired
				# print type(episode.FirstAired)
				if type(episode.FirstAired) != type(date.today()):					
					ep_date = (datetime.strptime(episode.FirstAired, "%Y-%m-%d")).toordinal()
				else:
					ep_date = (episode.FirstAired).toordinal()	
				# print "ep_date : "+(ep_date)
				# print "today : "+ (today)
				if ep_date < today - 1 : 				# - 1 to download episodes that are atleast a day old.
												
					if (len(show_data['seasons'][season_no]) < (episode.EpisodeNumber)):
						show_data['seasons'][season_no].append({})
				
					if show_data['seasons'][season_no][episode_no] == {}:
						episode_torrent = kat_search.get_tv_show_episode(show.SeriesName, season.season_number, episode.EpisodeNumber)						
						cur_ep = {"season":season.season_number, "episode":episode.EpisodeNumber}
						if episode_torrent == None:														
							if cur_ep not in show_data["erred_episodes"]:
								show_data["erred_episodes"].append(cur_ep)
								print "Adding to Errored episodes No torrent found"
							# show_data['seasons'][season_no][episode_no] = { 'magnet' : "", 'status' : "ERROR_no_magnet",'request_id' : 0, 'attempt' : 1}
							print("ERROR_no_magnet")
						else:							
							show_data['seasons'][season_no][episode_no] = start_episode_download(episode_torrent['magnet'], 0)
							if cur_ep in show_data["erred_episodes"]:
								show_data["erred_episodes"].remove(cur_ep)
							# print(show_data['seasons'][season_no][episode_no]["status"])													
					else:			
						cur_episode  = show_data['seasons'][season_no][episode_no]
						
						if cur_episode['status'] == "Error_retry":
							if cur_episode["attempt"] <= 5:
								show_data['seasons'][season_no][episode_no] = start_episode_download(cur_episode['magnet'], cur_episode["attempt"])							
							else:
								show_data['seasons'][season_no][episode_no] = { 'magnet' : "", 'status' : "ERROR_retry_failed",'request_id' : 0, 'attempt' : 5}
						else:
							#if (cur_episode['status']== "downloaded" ):
							#	print "downloaded succesfully"
							#elif (cur_episode['status'] != "ERROR_no_magnet") and (cur_episode['status'] != "ERROR_retry_failed"):
							if (cur_episode['status'] != "ERROR_no_magnet") and (cur_episode['status'] != "ERROR_retry_failed"):
								off_cloud_status = offcloud_api.get_torrent_status(cur_episode['request_id'])
								print (off_cloud_status['status'])
								if off_cloud_status['status']['status'] == "downloaded":
									show_data['seasons'][season_no][episode_no]['status'] = off_cloud_status['status']['status']
									print "send the follwing data to a google sheet"
									print "title " + show_data['title']
									print "season " + str(season.season_number)
									print  "episode " + str(episode.EpisodeNumber)
									print "if possible rename the file for convenience"

									# write code to push the directory structure to google sheets that will be used to organize the files	
								elif off_cloud_status['status']['status'] == "error":
									show_data['seasons'][season_no][episode_no]['status'] = "Error_retry"
									print "these downloads are in error state"
								#elif off_cloud_status['status']['status'] == "queued":									
				else:
					break
				json.dump(show_data, open(db_directory + show_file, 'w'))
				print("writing updated data to disk")
				
			json.dump(show_data, open(db_directory + show_file, 'w'))

if __name__ == '__main__':
	main(sys.argv)
