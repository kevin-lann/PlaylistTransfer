......# Playlist Transfer

This is a tool that allows you to transfer playlists between YT music and Spotify, using Spotify web API and ytmusic unofficial api.




# Setup

**Step 1: install ytmusicapi and spotipy**

```
pip install ytmusicapi
pip install spotipy
```

**Step 2: setup oauth for ytmusicapi**

After you install ytmusicapi, run

```
ytmusicapi oauth
```

This creates an oauth.json file in your current directory. Copy the contents of this oauth file and paste / replace the one in this project download.

**Step 3: setup keys for spotify WebAPI**

Go to https://developer.spotify.com/ and login with your desired Spotify account.
Go to dashboard and create a new project.
Go to settings > Basic Information.

Here you will find a client key and a client secret.
Copy those to the cred.py file in this project directory.
Do not alter the redirect URL.

```
CLIENT_ID = ''
CLIENT_SECRET = 'b'
REDIRECT_URL = 'http://localhost:8888/callback'
```


# Running

THe script takes a single command-line argument. For transferring a playlist to Spotify, use "sp". Likewise, for transferring a playlist to Youtube Music, use "yt".

eg.

```
python .\PlaylistTransfer.py yt
```


