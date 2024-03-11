''' In this file, I will be creating a dataframe containing information about the artists who have won the Grammys 
Best New Artist award and the albums they have released. To do this, I will load the csv file containgint he iwnners and utilize 
the Spotify API to gather the information needed (album name, album release date, album type )

To produce the Spotify API code, I followed the Youtube video titled "How to Use Spotify's API with Python | Write a 
Program to Display Artist, Tracks, and More" by Akamai Developer. 
'''


from dotenv import load_dotenv
import os
import requests
import base64
from requests import post, get
import json
import pandas as pd


#reading in the Best New Artist Winners csv file and converting to a dataframe
grammy_best_new = pd.read_csv("~/Desktop/capstone/data/best_new2.csv")
best_new_df = pd.DataFrame(grammy_best_new)

#isolating the artist winners
best_new_winners = best_new_df['artist_name']

# loop through the artists to get their spotify information

artist_name = []
album_name = []
album_date = []
album_type = []


#spotify API functions

# function to get access to authorization token 

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


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


for name in best_new_winners:

    token = get_token()
    result = search_for_artist(token, f'{name}')

    artist_id = result["id"]

    album_name_api = get_artist_album_names(token, artist_id)

    album_date_api = get_artist_album_date(token, artist_id)

    album_type_api = get_artist_album_type(token, artist_id)

    artist_name.append(name)
    album_name.append(album_name_api)
    album_date.append(album_date_api)
    album_type.append(album_type_api)


# Creating a DataFrame
data = {
    'artist_name': artist_name,
    'album_names': album_name,
    'release_date': album_date,
    'type': album_type,
}

df = pd.DataFrame(data)
df

#Save the DataFrame to a CSV file
df.to_csv('artist_album_info', index=False)


    