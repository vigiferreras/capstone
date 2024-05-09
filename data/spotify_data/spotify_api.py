''' In this file, I practiced getting my Spotify API token and getting the information needed)

To produce the Spotify API code, I followed the Youtube video titled "How to Use Spotify's API with Python | Write a 
Program to Display Artist, Tracks, and More" by Akamai Developer. 
 '''

from dotenv import load_dotenv
import os
import requests
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# function to get access to authorization token 
def get_token():

    # concatenate client id and client secret
    auth_string = client_id + ":" + client_secret

    # encode
    auth_bytes = auth_string.encode("utf-8")

    # encode again
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") #base 64 object converted to string to pass with headers when we send out request

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    # body of the request
    result = post(url, headers = headers, data = data)

    # convert json data to python dictionary 
    json_result = json.loads(result.content)

    #parse token
    token = json_result["access_token"]

    return token

# function to constuct the header needed
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# function to search for artist 
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search" #found from spotify web developer site
    headers = get_auth_header(token)

    # constructing query
    query = f"?q={artist_name}&type=artist&limit=1" #note limit =1 will find the first artist with the same/similar name

    query_url = url + query

    result = get(query_url, headers = headers)

    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name exists!")
        return None
    
    return json_result[0]

# get top tracks 
def get_songs_by_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_artist_genre(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["genres"]
    return json_result

def get_artist_followers(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["followers"]["total"]
    return json_result

def get_artist_popularity(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["popularity"]
    return json_result

def get_artist_album_names(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["items"]

    album_names = [album['name'] for album in json_result]
    
    return album_names

def get_artist_album_type(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["items"]

    album_type = [album['album_type'] for album in json_result]
    
    return album_type

def get_artist_album_date(token, artist):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["items"]

    album_year = [album['release_date'] for album in json_result]
    
    return album_year


# tests
token = get_token()
result = search_for_artist(token, "Ariana Grande")
print(result["name"])

artist_id = result["id"]

songs = get_songs_by_artists(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}, {song['name']}")

artist_genre = get_artist_genre(token, artist_id)
print(artist_genre)

artist_followers = get_artist_followers(token, artist_id)
print(artist_followers)

artist_pop = get_artist_popularity(token, artist_id)
print(artist_pop)

artist_albums = get_artist_album_names(token, artist_id)
print(artist_albums)

artist_album_year = get_artist_album_date(token, artist_id)
print(artist_album_year)

artist_album_type = get_artist_album_type(token, artist_id)
print(artist_album_type)