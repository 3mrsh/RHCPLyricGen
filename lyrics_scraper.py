# execfile("")

from bs4 import BeautifulSoup
import requests

'''
---------------------------------
Function Definitions:
--------------------
'''

def getAlbumsList():
	albums_page_url = "https://redhotchilipeppers.com/audio"
	r = requests.get(albums_page_url)
	soup = BeautifulSoup(r.text, 'html.parser')
	photos = soup.select('a.media-grid-item.photo')
	return map(lambda x: [x.text.strip(), x.get('href')], photos)

def formatTrackNames(track_number, track_name):
	return "#" + str(track_number) + ". " + track_name.encode('utf8')

def extractSongLyrics(all_lyrics_entry):
	# Maintain structure by first dividing it into the p tags
	u_stanzas = all_lyrics_entry.select('p')
	s_stanzas = map(lambda x: x.get_text().encode('utf8').split("\xc2\xa0"*8), u_stanzas)
	map(lambda x: x[0]=='' and x.pop(0), s_stanzas)
	return s_stanzas

def writeToFile(formatted_track_name, lyrics):
	if lyrics == []:
		print "no lyrics found for: ", formatted_track_name
	f.write("\n"+formatted_track_name + "\n")
	f.write("Songwriters: \nCover: \n\n")
	for stanza in lyrics:
		map(lambda line: f.write(line + "\n"), stanza)
		f.write("\n")
	f.write("-----------\n")


'''
---------------------------------
Code:
--------------------
'''

albumsList = getAlbumsList()
for (albumName, albumUrl) in albumsList:
	f = open("Lyrics/"albumName+".lyrics","w")
	r = requests.get(albumUrl)
	soup = BeautifulSoup(r.text, 'html.parser')

	release_date = soup.select("div.hive-date")[0].text.strip().split("Released: ")[1]

	f.write(release_date+"\n-----------------\n")

	track_names = map(lambda x: x.text, soup.select('div.audio-track-list-item-title'))
	formattedTrackNames = map(formatTrackNames, range(1, len(track_names)+1), track_names)

	raw_lyrics = soup.select('div.audio-track-list-item-lyrics')
	extracted_lyrics = map(extractSongLyrics, raw_lyrics)

	map(writeToFile, formattedTrackNames, extracted_lyrics)

	f.close()

