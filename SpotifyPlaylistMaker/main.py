
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
token = os.getenv('ACCESS_TOKEN')
SONGS_URL = 'https://www.billboard.com/charts/hot-100/'
scope = "playlist-modify-public"

auth_manager = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            scope=scope,
                            redirect_uri='http://example.com')

sp = spotipy.Spotify(auth_manager=auth_manager)
user_id = sp.current_user()['id']



def get_date():
    input_string = ""
    def check():
        return len(input_string) < 10 or len(input_string) > 10
    while check():
        input_string = input("Enter a date to create a playlist! (e.g. YYYY-MM-DD) ")
        if check():
            print("Bad input! Try again!")
    return input_string


def get_top_songs(date):
    response = requests.get(f"{SONGS_URL}{date}/)")
    soup = BeautifulSoup(response.text, 'html.parser')

    song_groups = [list(song.parent.children) for song in soup.select(selector="li h3", class_="c-title")]
    song_groups = song_groups[:100]

    songs_name = [group[1].getText().strip() for group in song_groups]
    artist_names = [group[3].getText().strip() for group in song_groups]
    year = date.split('-')[0]

    queries = []
    for index in range(100):
        queries.append(f"{songs_name[index]}%{artist_names[index]}%{year}")

    return queries


def create_playlist(playlist_name):

    playlist_desc = f"A playlist for '{playlist_name}' "
    playlist = sp.user_playlist_create(user_id,
                                       playlist_name,
                                       public=True,
                                       description=playlist_desc)
    return playlist['id']


def search_and_add(playlist_id, query):
    try:
        results = sp.search(q=query, type='track', limit=1)
        track_uri = results['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist_id, items=[track_uri])
    except KeyError:
        return

def main():
    date = get_date()
    queries = get_top_songs(date)
    playlist_name = f"Billboard {date}"
    playlist_id = create_playlist(playlist_name)
    for query in queries:
        print(f"Checking -> {query}")
        search_and_add(playlist_id, query)
    print(f"Songs added!")


if __name__ == '__main__':
    main()


# def get_token():
#     auth_string = client_id + ':' + client_secret
#     auth_bytes = auth_string.encode('utf-8')
#     auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
#
#     url = 'https://accounts.spotify.com/api/token'
#     headers = {
#         'Authorization': 'Basic ' + auth_base64,
#         "Content-Type": 'application/x-www-form-urlencoded'
#     }
#     data = {"grant_type": "client_credentials"}
#
#     response = requests.post(url, headers=headers, data=data)
#     json_result = json.loads(response.content)
#     token = json_result['access_token']
#     print(token)
