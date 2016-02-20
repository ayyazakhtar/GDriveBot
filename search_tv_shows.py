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

db_name = "torrent_db"
def get_new_show_input():
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
		show_data = {'title':show.SeriesName, 'imdb_id':show.IMDB_ID, 'cur_season': 1, 'cur_episode':0}
		show.update()
		json.dump(show_data, open("tv_show_" + show.SeriesName.replace(' ', '_')+ ".json", 'w'))
		break
		
db = api.TVDB("B43FF87DE395DF56")

if len(sys.argv) > 1:
	if sys.argv[1] == 'add':
		get_new_show_input()

		

# con = lite.connect(db_name)

	
# with con:    
	# con.row_factory = lite.Row
	# cur = con.cursor()
	
	# cur.execute("CREATE TABLE IF NOT EXISTS tvshows( imdb_id TEXT, show_title TEXT, season INT, episode INT, episode_title TEXT, status TEXT, offcloud_ref_no INT, magnet_link Text)")
	
	# cur.execute("CREATE TABLE IF NOT EXISTS movies( imdb_id TEXT, movie_title TEXT, status TEXT, offcloud_ref_no INT)")

	# # cur.execute("INSERT INTO Cars VALUES(2,'Audi',52642)")
	# # cur.execute("INSERT INTO Cars VALUES(1,'Mercedes',57127)")
	
	# # cur.execute("SELECT * FROM Cars")
	# # cur.execute("SELECT * FROM Cars WHERE Id=? ", ("1")) 
	# # rows = cur.fetchall()

	# # for row in rows:
		# # print row

# exit()

file_list = []

for file in os.listdir('.'):
	if fnmatch.fnmatch(file, 'tv_show_*.json'):
		file_list.append(file)
		

for show_file in file_list:
	show_data = json.load(open(show_file))	
	show = db.get_series( show_data["imdb_id"], "en" , id_type='imdb', cache=True)
	show.update()
	print '-------------------' + str(show.SeriesName) + ' ------------------------'
	for season in show:
		if season.season_number == 0:
			continue
		print '--------------- Season' + str(season.season_number) + ' --------------------'
		for episode in season:	
			today = (date.today()).toordinal()
			ep_date = (episode.FirstAired).toordinal()
			if ep_date < today + 1 : # to download episodes that are atleast a day old.
				print '----------- Episode ' + str(episode.EpisodeNumber) + ' ----------------'
				print(u"{0} - {1}".format(episode.EpisodeName, episode.FirstAired)) 
				#episode_torrent = kat_search.get_tv_show_episode(show.SeriesName, season.season_number, episode.EpisodeNumber)
				#print episode_torrent['name']
		
	exit()

exit()

 
