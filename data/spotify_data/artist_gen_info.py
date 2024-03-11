''' In this file, I will be creating a dataframe containing genreal information about the artists who have won the Grammys 
Best New Artist award. To do this, I will load the csv file containgint he iwnners and utilize the Spotify API to gather the information needed
(genre, followers, and populairty)

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
artist_genre = []
artist_followers = []
artist_popularity = []


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



for name in best_new_winners:

    token = get_token()
    result = search_for_artist(token, f'{name}')

    artist_id = result["id"]

    artist_genre_api = get_artist_genre(token, artist_id)

    artist_followers_api = get_artist_followers(token, artist_id)

    artist_popularity_api = get_artist_popularity(token, artist_id)

    artist_name.append(name)
    artist_genre.append(artist_genre_api)
    artist_followers.append(artist_followers_api)
    artist_popularity.append(artist_popularity_api)


# Creating a DataFrame
data = {
    'artist_name': artist_name,
    'genre': artist_genre,
    'followers': artist_followers,
    'popularity': artist_popularity,
}

df = pd.DataFrame(data)
df

#Save the DataFrame to a CSV file
df.to_csv('artist_general_info.csv', index=False)


    
   
