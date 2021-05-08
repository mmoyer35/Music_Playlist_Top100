import requests
import pprint
import spotipy as spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

# Credentials, you will need your own ID and Key
SPOTIPY_CLIENT_ID= "SPOTIPY_CLIENT_ID"
SPOTIPY_CLIENT_SECRET="SPOTIPY_CLIENT_SECRET"
SPOTIPY_REDIRECT_URI='http://example.com'
uri_list = []

#Log into spotify
pp = pprint.PrettyPrinter(indent=4)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                        client_secret=SPOTIPY_CLIENT_SECRET,
                                        redirect_uri=SPOTIPY_REDIRECT_URI,
                                        state=None, cache_path=".cache", username=None, scope="playlist-modify-private",
                                        proxies=None, show_dialog=True, requests_session=True, requests_timeout=None))



user_id = sp.current_user()["id"]

# Insert date, create playlist for the Billboard Top 100 songs on that date
playlist_date = input("What time would you like to travel back to (in YYYY-MM-DD format)? ")
song_year = playlist_date.split("-")[0]
response = requests.get(f"https://www.billboard.com/charts/hot-100/{playlist_date}")
billboard_date = response.text

# Make soup
soup = BeautifulSoup(billboard_date, "html.parser")
#Create song list
songs = [song.getText() for song in soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")]
song_uris = []

#Create song URI list, print out index error if the song isn't available.
for song in songs:
    result = sp.search(q=f"track:{song} year:{song_year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
#Create playlist
playlist_name = f"{playlist_date} Playlist"
new_playlist = sp.user_playlist_create(user_id, name=playlist_name, public=False)
# playlist = sp.user_playlists(user_id)


sp.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris)
