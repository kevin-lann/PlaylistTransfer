import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from ytmusicapi import YTMusic
import sys


def invalid_optn(): print("Invalid optn: please enter \"sp\" or \"yt\".")


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


# for testing
def print_results(search_results):
    for result in search_results:
        print(result["name"] + " by " + result["artists"][0]["name"])
    print("")


'''
Current search mtd: search top results until first instance with track title in name (or vice versa) and
artist name found in the track artist list or the track title itself.

If result found, return track uri
If no result found, then notify user in terminal and return None.
'''
def best_search_result(source, search_results, track_name, artist_name):
    if source == "sp":
        for track in search_results:
            if ((track_name in track["name"] or track["name"] in track_name) and 
                (track["artists"][0]["name"] in artist_name or artist_name in track["artists"][0]["name"] or artist_name in track["name"])):
                return track["uri"]
        else:
            print("Track not found: " + track_name + " by " + artist_name)
            return None
    
    elif source == "yt":
        for track in search_results:
            if((track_name in track['title'] or track['title'] in track_name) and
               (track["artists"][0]["name"] in artist_name or artist_name in track["artists"][0]["name"] or artist_name in track['title'])):
                return track["videoId"]
        else:
            print("Track not found: " + track_name + " by " + artist_name)
            return None

    else: invalid_optn()


def create_playlist(source, track_list, name):
    user_id = sp.current_user()["id"]
    playlist = {}
    items = []

    if source == "sp":
        playlist = sp.user_playlist_create(user_id, name, public=False, collaborative=False)

        for track_name, artist_name in track_list:
            search_results = sp.search(track_name + " " + artist_name, limit=10, offset=0, type='track', market=None)
            # print_results(search_results["tracks"]["items"])
            best_result = best_search_result("sp", search_results["tracks"]["items"], track_name, artist_name)
            if(best_result != None): items.append(best_result)

        sp.playlist_add_items(playlist["id"], items, position=None)

    elif source == "yt":
        playlist_id = ytm.create_playlist(name, "", 'PRIVATE')
        
        for track_name, artist_name in track_list:
            search_results = ytm.search(track_name, "songs", scope=None, limit=10, ignore_spelling=False)
            best_result = best_search_result("yt", search_results, track_name, artist_name)
            if(best_result != None): items.append(best_result)
        
        ytm.add_playlist_items(playlist_id, items)
    
    else: invalid_optn()
        
    print("Playlist generated.")
    

if __name__ == "__main__":
    to_ = sys.argv[1]
    if to_ == "sp": from_="yt"
    elif to_ == "yt": from_ = "sp"
    else: invalid_optn() or exit()

    # SETUP 
    scope = "playlist-modify-private"

    auth_mgr = SpotifyOAuth(client_id=cred.CLIENT_ID, 
                            client_secret=cred.CLIENT_SECRET,
                            redirect_uri=cred.REDIRECT_URL,
                            scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_mgr)

    ytm = YTMusic("oauth.json")

    # Convert
    print_playlist_names(from_)

    print("\nChoose a playlist you would like to copy from:\n")
    playlist_name = input()

    track_list = []
    track_list = get_playlist_tracks(from_, playlist_name)

    create_playlist(to_, track_list, playlist_name)



