from dotenv import load_dotenv
import requests 
import os
import webbrowser
import json

load_dotenv()

# pulled from .env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = "playlist-modify-public playlist-modify-private user-library-read user-library-modify user-top-read playlist-read-private playlist-read-collaborative"

auth_url = (
    "https://accounts.spotify.com/authorize?"
    + "response_type=code"
    + "&client_id=" + CLIENT_ID
    + "&redirect_uri=" + REDIRECT_URI
    + "&scope=" + SCOPES
)

options = f"(1) List playlists\n(2) List top artists\n(3) List top tracks\n(4) Get track audio features\n(5) Get track audio analysis"

def get_authorization_header(token):
    return {"Authorization": "Bearer " + token}

# Login to Spotify and get access token
def login():
    print("Please log in to Spotify for authentication.")
    webbrowser.open(auth_url)
    auth_code = input("Enter the authorization code: ")

    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    token_response = requests.post(token_url, data=payload)
    token_info = token_response.json()
    
    if "access_token" in token_info:
        profile_url = "https://api.spotify.com/v1/me"
        headers = get_authorization_header(token_info["access_token"])
        profile_response = requests.get(profile_url, headers=headers)
        profile_info = profile_response.json()
        return token_info["access_token"], profile_info["display_name"]
    else:
        print("Failed to retrieve access token. Try Again")
        return None, None

# Get all user playlists
def get_user_playlists(token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = get_authorization_header(token)
    result = requests.get(url, headers=headers)

    if result.status_code == 200:
        for playlist in json.loads(result.content)["items"]:
            print(playlist["name"])
    else:
        print(f"Error fetching playlists.")

# Get user top artists
def get_user_top_artists(token):
    url = "https://api.spotify.com/v1/me/top/artists"
    headers = get_authorization_header(token)
    result = requests.get(url, headers=headers)

    if result.status_code == 200:
        for artist in json.loads(result.content)["items"]:
            print(artist["name"])
    else:
        print(f"Error fetching top artists.")

# Get user top tracks
def get_user_top_tracks(token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = get_authorization_header(token)
    result = requests.get(url, headers=headers)

    if result.status_code == 200:
        for track in json.loads(result.content)["items"]:
            print(track["name"] + " by " + track["artists"][0]["name"])
    else:
        print(f"Error fetching top tracks.")

# Search for track, return track json object
def search_track(token):
    track_name = input("Enter the track name: ")
    url = f"https://api.spotify.com/v1/search?q={track_name}&type=track"
    headers = get_authorization_header(token)
    result = requests.get(url, headers=headers)

    if result.status_code == 200:
        return json.loads(result.content)["tracks"]["items"][0]
    else:
        print(f"Error searching for track. Try Again.")
        return None

# # Get audio analysis for track
# def get_audio_analysis(token):
#     track = search_track(token)
#     while track is None:
#         track = search_track(token)
#     track_id = track["id"]
#     print(track_id)

#     url = f"https://api.spotify.com/v1/audio-features/{track_id}"
#     headers = get_authorization_header(token)
#     result = requests.get(url, headers=headers)

#     if result.status_code == 200:
#         audio_analysis = json.loads(result.content)
#         print(audio_analysis)
#     else:
#         error_details = result.json()  # Get the error response in JSON format
#         error_message = error_details.get("error", {}).get("message", "No message provided")
#         error_reason = error_details.get("error", {}).get("reason", "No reason provided")
#         print(f"Error {result.status_code}: {error_message}. Reason: {error_reason}")

# # Get audio features for track
# def get_audio_features(token):
#     track = search_track(token)
#     while track is None:
#         track = search_track(token)
#     track_id = track["id"]
#     url = f"https://api.spotify.com/v1/audio-features/{track_id}"
#     headers = get_authorization_header(token)
#     result = requests.get(url, headers=headers)

#     if result.status_code == 200:
#         audio_features = json.loads(result.content)
#         print(audio_features)
#     else:
#         print(f"Error fetching audio features.")


user_functions = [get_user_playlists, get_user_top_artists, get_user_top_tracks]

access_token, account_name = login()
while access_token is None:
    access_token, account_name = login()
print(f"Welcome {account_name}!")

while True:
    desired_operation = int(input(f"-\n{options}\nChoose an option (1-3): "))
    user_functions[desired_operation - 1](access_token)