from pytvdbapi import api

db = api.TVDB("B43FF87DE395DF56")
#results = db.search("the flash 2014", "en")
#for result in results:
#    print(result.SeriesName)

show = db.get_series( 1796960, "en" , id_type='imdb', cache=True)  # Load Dexter
print(show.SeriesName)

#show = results[0];
#tt2193021
count = 0
for season in show:
    if season.season_number == 0:
        continue;
    print '--------------- season ' + str(season.season_number) + ' --------------------'
    for episode in season:
        print(u"{0} - {1}".format(episode.EpisodeName, episode.FirstAired))  
