import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from ytmusicapi import YTMusic

def invalid_optn(): print("Invalid optn: please enter sp or yt.")

def get_user_recently_played(source):
    if source == "sp":
        results = sp.current_user_recently_played()
        for item in results['items']:
            track = item['track']
            print(track['artists'][0]['name'], " - ", track["name"])
    elif source == "yt":
        for item in ytm.get_history():
            print(item['artists'][0]['name'], " - ", item["title"])
    else: invalid_optn()

def print_playlist_names(source):
    if source == "sp":
        playlists = sp.current_user_playlists(limit=None, offset=0)
        for playlist in playlists["items"]:
           print(playlist["name"] + " (" + str(playlist["tracks"]["total"]) + " tracks)")
    elif source == "yt":
        playlists = ytm.get_library_playlists(limit=None)

        for playlist in playlists:
            if("count" not in playlist.keys()): print(playlist["title"])
            else: print(playlist["title"] + " (" + playlist["count"] + " tracks)")

    else: invalid_optn()

def get_playlist_tracks(source, playlist_name):
    tracks = [] # [(name, artist)]
    target_playlist = {}

    if source == "sp":
        playlists = sp.current_user_playlists(limit=None, offset=0)["items"]
        for playlist in playlists:
            if playlist["name"] == playlist_name:
                playlist_id = playlist["id"]
                username = sp.current_user()["id"]
                target_playlist = sp.user_playlist(username, playlist_id)
                break
        else:
            print("Error: playlist name not found. Please check spelling.")
            exit()

        for track in target_playlist['tracks']['items']:
            tracks.append((track['track']['name'], track['track']['artists'][0]['name']))

    elif source == "yt":
        playlists = ytm.get_library_playlists(limit=None)
        for playlist in playlists:
            if playlist["title"] == playlist_name:
                playlist_id = playlist["playlistId"]
                target_playlist = ytm.get_playlist(playlist_id, None)
                break
        else:
            print("Error: playlist name not found. Please check spelling.")
            exit()

        for track in target_playlist["tracks"]:
            tracks.append((track["title"], track["artists"][0]["name"]))

    else: invalid_optn()

    return tracks

def create_playlist(source):
    pass



# SETUP 

scope = "user-read-recently-played"

auth_mgr = SpotifyOAuth(client_id=cred.CLIENT_ID, 
                        client_secret=cred.CLIENT_SECRET,
                        redirect_uri=cred.REDIRECT_URL,
                        scope=scope)
sp = spotipy.Spotify(auth_manager=auth_mgr)

ytm = YTMusic("oauth.json")

# Convert

print_playlist_names("yt")

print("\nChoose a playlist you would like to copy from:\n")
playlist_name = input()

track_list = []
track_list = get_playlist_tracks("yt", playlist_name)
print(track_list)
