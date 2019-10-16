import csv 
import matplotlib.pyplot as plt
import json


"""

READ AND STORE .CSV FILE AS {top_500_albums}, a list of dicts.

Each element of the list takes the following form:

    {'number':{rank}, 'name':{album title}, 'artist':{artist name}, 
     'genre':{list of genres}, 'subgenre':{list of subgenres}}

Years and ranks are ints. Everything else is strings or lists of strings.

Attempts to clean genre and subgenre data.

"""

with open('data.csv') as f:
    reader = csv.DictReader(f)
    top_500_albums = [{'number':int(row['number']),
                  'year':int(row['year']),
                  'name':row['album'],
                  'artist':row['artist'],
                  'genre':row['genre'].split(','),
                  'subgenre':row['subgenre'].split(',')}
                for row in reader]
    for album in top_500_albums:
        for index in list(range(0,len(album['genre']))):
            album['genre'][index] = album['genre'][index].strip()
        for index in list(range(0,len(album['subgenre']))):
            album['subgenre'][index] = album['subgenre'][index].strip()

"""

READ AND STORE .txt FILE AS {top_500_songs}, a list of dicts.

Each element in the list takes the following form:
    
    {'number':{rank}, 'name':{song title}, 
    'artist':{artist name}, 'year':{year}}

All years and ranks are ints. Everything else is strings.

"""
    
text_file = open('top-500-songs.txt', 'r')
    # read each line of the text file
    # here is where you can print out the lines to your terminal and get an idea 
    # for how you might think about re-formatting the data
lines = text_file.readlines()
    # lines is a list of strings, each element is a new line
    
def unformatted_songs_list():
    new_list = [line.split('\t') for line in lines]
    for line in new_list:
        line[3] = line[3][:4]
    return new_list

top_500_songs = [{'number':int(song[0]), 
                  'name':song[1],
                  'artist':song[2], 
                  'year':int(song[3])} for song in unformatted_songs_list()]    
    
"""

READ AND STORE JSON FILE AS {albums_songs}, a list of dicts that contains all
of the song titles in every album in {top_500_albums}.

Each element of the list takes the following form:
    
    {'artist':{artist name}, 'album':{album title}, 
    'tracks': {list of tracks on album}}

All are strings except tracks, which is a list lists of strings.


"""

file = open('track_data.json', 'r')
albums_songs = json.load(file)


#print(albums_songs[0])

"""

FUNCTIONS FOR USE ON ABOVE DATA

"""
    
    
def find_by_name(title, data):
    """
    Returns the song or album info from {data} that has title {title}.
    If no elements with that title, returns None.
    """
    for element in data:
        if element['name'] == title:
            return album
    return None

def find_by_rank(rank, data):
    """
    Returns the song or album info from {data} that has rank {rank}.
    If no elements with that rank, returns None.
    """
    for element in data:
        if element['number'] == rank:
            return element
    return None

def find_by_year(year, data):
    """
    Returns a list of songs or albums from {data} released in year {year}.
    If no elements from that year, returns empty list.
    """
    return [element 
              for element in data 
              if element['year'] == year]


def find_by_years(start_year, end_year, data):
    """
    Returns a list of songs or albums from {data} released between {start_year}
    and {end_year}. If no elements from those years, returns empty list.
    """
    result = []
    for year in list(range(start_year,end_year+1)):
        result.extend(find_by_year(year,data)) 
    return result if result else []

def find_by_ranks(start_rank, end_rank, data):
    """
    Returns a list of songs or albums from {data} with ranks between 
    {start_rank} and {end_rank}. If no elements from those years, returns 
    empty list.
    """
    result = [find_by_rank(rank) for rank in list(range(start_rank,end_rank+1)) if find_by_rank(rank)]
    return result if result else []
        
def all_titles(data):
    """
    Returns a list of all song or album titles from {data}.
    """
    return [element['album'] for element in data]
    
def all_artists(data):
    """
    Returns a list of all artist names from {data}.
    """
    return [song['artist'] for song in songs]

def top_artist(data):
    """
    Returns the name of the artist with the highest number of appearances in
    {data}.
    """
    uniq_artists = list(set(all_artists(data)))
    counts = {}
    for artist in uniq_artists:
        counts[artist] = all_artists(data).count(artist)
    
    count = 0
    top = None
    for key, value in counts.items():
        if value > count:
            count = value
            top = key
    return top

def most_popular_word(data):
    """
    Returns the word with the highest number of appearances in titles in {data}.
    """
    all_words = []
    for title in all_titles():
        all_words.extend(title.lower().split())
    uniq_words = list(set(all_words))
    counts = {}
    for word in uniq_words:
        counts[word] = all_words.count(word)
    count = 0
    top = None
    for key, value in counts.items():
        if value > count:
            count = value
            top = key  
    return top


decades = [(1950,1959), (1960,1969), (1970,1979),
           (1980,1989),(1990,1999), (2000,2009),(2010,2019)]
"""
{decades} for use in histograms  

"""

def plot_hist_albums(data):
    """
    Plots a histogram of the number of albums from {data} released per decade.
    """
    global decades
    hist_data = {}
    mid_decade_yr = []
    for decade in decades:
        hist_data[f'{decade[0]} - {decade[1]}'] = len(find_by_years(decade[0],
                                                         decade[1],data))
        mid_decade_yr.append(decade[0]+5)
    decades = []
    for key, value in hist_data.items():
        decades.append(key)

    all_years = [song['year'] for song in songs]
        
    plt.figure(figsize =(10,6))
    plt.hist(all_years,bins=8, edgecolor = 'black')
    plt.axis([1950,2020,0,200])
    plt.xticks(mid_decade_yr,mid_decade_yr)
    plt.xlabel('Year')
    plt.ylabel('Number of Albums')
    plt.title('Albums released by year')
    plt.show()

#plot_hist_albums(albums)

def numberOfSongs():
    """
    Count how many songs there are in total in albums_songs - There are 7375.
    It has len 478, meaning that each album here is just the albums on 
    {top_500_alumbs}, which has the exact same length.
    """
    global albums_songs
    count = 0
    for album in overlapping_songs:
        count += len(album['tracks'])
    return count    

def album_with_most_top_songs():
    """
    Identify top artist. Generate a list of all of their top songs.
    Generate a list of their top albums. Then create a sublist from albums_songs
    that include only the albums and songs from the top artist. Iterate through
    that sublist to count the number of songs in each album that appear in
    the list of the top artist's top_500_songs. 
        {'album1':count, 'album2':count, ...}
    return the album with highest count
    """
    top_artist_name = top_artist(top_500_songs)
    top_artist_songs = [song['name'] for song in top_500_songs if song['artist'] == top_artist_name]
    top_artist_albums = [album['name'] for album in top_500_albums if album['artist'] == top_artist_name]
    top_albums_with_tracks = [album for album in albums_songs if album['album'] in top_artist_albums]
    """
    iterate through top albums. Creates dict with each album and how many songs
    in it appear in top_500_songs:
        
        
    """
    
    counter = {}
    for entry in top_albums_with_tracks:
        counter[entry['album']]=0
        for track in entry['tracks']:
            if track in top_artist_songs:
                counter[entry['album']] += 1
    key = None
    value = 0    
#    print(counter)      
    for k, v in counter.items():
        print((k, v))
        if v > value:
            key = k
            value = v
    
    return {top_artist_name:key}

def albums_with_top_songs():
    """
    returns a list with the name of only the albums that 
    have tracks featured on the list of top 500 songs
    
    Create list of songs on top_500_songs. Iterate through list of albums_songs
    to see if those songs are in top albums. If yes, add album name to a new list.
    Create a set of the result to return a list with unique entries.
    
    """
    top_500_song_list = [song['name'] for song in top_500_songs]
    albums_with_top_songs = [album['album'] for album in albums_songs for track in album['tracks'] if track in top_500_song_list]
    return list(set(albums_with_top_songs))

#print(albums_with_top_songs())

def songs_that_are_on_top_albums():
    """
    Returns a list with the name of only the songs featured on the list 
    of top albums
    
    Create list of songs on top_500_songs. Iterate through list of albums_songs
    to see if those songs are in top albums. If yes, add song name to a new 
    list that will be returned.
   
    """
    top_500_song_list = [song['name'] for song in top_500_songs]
    return [track for album in albums_songs for track in album['tracks'] if track in top_500_song_list]
    
def top_10_albums_by_song():
    """
    Returns a histogram with the 10 albums that have the most songs that appear 
    in the top songs list. The album names should point to the number of songs 
    that appear on the top 500 songs list.
    """
    pass

def top_overall_artist():
    """
    Returns the aritst featured with the most songs and albums on the two lists. This means 
    that if Brittany Spears had 3 of her albums featured on the top albums 
    listed and 10 of her songs featured on the top songs, she would have a 
    total of 13. The artist with the highest aggregate score would be the 
    top overall artist.
    
    """
    all_artists_in_albums = all_artists(top_500_albums)
    counter = {}
    for artist in all_artists_in_albums:
        counter[artist] = all_artists_in_albums.count(artist)
    
    for song in top_500_songs:
        if counter.get(song['artist']) == None:
            counter[song['artist']] = 1
        else:
            counter[song['artist']] += 1
    
    key = None
    value = 0
    
    for k, v in counter.items():
        if v > value:
            value = v
            key = k
            
    return key
#print(albums_songs[0])
#print(songs_that_are_on_top_albums())
print(top_overall_artist())
