from dotenv import load_dotenv
from google.cloud import storage
import os
import pandas as pd
import requests
import json
import time

load_dotenv()

class Spotify_API():
    def __init__(self):
        # Initialize your variables here
        self.base_64 = os.getenv("BASE64")
        self.refresh_token = os.getenv("REFRESH_TOKEN")
        self.token_expiration_time = os.getenv("EXPIRATION_TIME") 
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.bucket_name = 'practice17'

    def token_expired(self):
        # Implement your token expiration check logic
        current_time = int(time.time())
        expiration_time = self.token_expiration_time  # Function to retrieve the expiration time of the token
        return current_time >= int(expiration_time)

    def refresh(self):
        # Implement your token refresh logic
        # Code to refresh the access token
        token_endpoint = "https://accounts.spotify.com/api/token" #url

        response = requests.post(token_endpoint,
                                    data={"grant_type": "refresh_token",
                                        "refresh_token": self.refresh_token},
                                    headers={"Authorization": "Basic " + self.base_64})
        print("Refreshing access token...")

        response_json = response.json()
        return response_json
        print("access token refreshed")
        # Perform the necessary steps to refresh the access token

    def perform_task(self):
        # Retrieve the access token and perform the task
        if self.token_expired():
            res = self.refresh()
            self.access_token = res['access_token']

        current_timestamp = int(time.time())
        seven_days_ago_timestamp = current_timestamp - (7 * 24 * 60 * 60)
        past_7_days_unix_timestamp = seven_days_ago_timestamp * 1000

        endpoint = "https://api.spotify.com/v1/me/player/recently-played"
        head = {"Authorization": "Bearer " + self.access_token}

        params = {
            "limit": 50,
            "after": past_7_days_unix_timestamp
        }

        all_songs = []

        while True:
            r = requests.get(endpoint, headers=head, params=params)
            response = r.json()

            for item in response['items']:
                song_name = item['track']['name']
                played_at = item['played_at'][0:16].split('T')
                played_at = " ".join(played_at)
                artists = [artist['name']+"-"+artist['uri']for artist in item['track']['artists']]
                popularity = item['track']['popularity']
                album_type = item['track']['album']['album_type']
                if album_type == 'album':
                    album_type = "Yes"
                else:
                    album_type = "No"

                all_songs.append({
                    'played_at': played_at,
                    'song_name': song_name,
                    'artist': artists,
                    'popularity': popularity,
                    "belong_to_album": album_type
                })

            if 'next' in response:
                if response['cursors'] is not None and 'after' in response['cursors']:
                    params['after'] = response['cursors']['after']
                else:
                    break
            else:
                break

        df = pd.DataFrame(all_songs)
        df.to_csv('/home/krissemmy17/Exam-Project/spoti-data/recently_played_songs.csv', index=False)
        print("CSV file successfully created.")

    def feature_eng(self):
        # Implement your feature engineering logic
        file_name = "/home/krissemmy17/Exam-Project/spoti-data/recently_played_songs.csv"
        df = pd.read_csv(file_name)
        df["song_name"] = df["song_name"].apply(lambda x: x.split("(")[0])
        df["artist_uri"] = df["artist"].copy()
                
        def get_artist(x):
            x = eval(x)
            if len(x) == 1:
                x1 = x[0].split("-s")[0]
                return x1
            elif len(x) > 1:
                x2 = [i.split("-s")[0] for i in x] 
                # x2 = x2[1:]
                return x2

        df["artist"] = df["artist"].apply(get_artist)

        def get_uri(x):
            x = eval(x)
            if len(x) == 1:
                x1 = x[0].split("-s")[1]
                x1 = 's'+x1
                return x1
            elif len(x) > 1:
                x2 = ['s'+i.split("-s")[1] for i in x] 
                return x2

        df["artist_uri"] = df["artist_uri"].apply(get_uri)


        df["artist_featured"] = df["artist"].copy()
        def feature(x):
            if isinstance(x, list):
                x1 = x[1:]
                if len(x1) == 1:
                    return x1[0]
                else:
                    return x1
            else:
                return "None"
                
        def art(x):
            # x = x.split("[")
            if isinstance(x, list):
                x = x[0]
                return x
            else:
                return x

        df['artist'] = df['artist'].apply(art)

        df['artist_featured'] = df['artist_featured'].apply(feature)   
        df.to_csv("/home/krissemmy17/Exam-Project/spoti-data/2023_06_19_to_2023_06_26.csv", index=False)

    def upload_to_storage(self):
        # Implement your file upload logic to Google Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        
        blob = bucket.blob("2023_07_09_to_2023_07_16.csv")
        blob.upload_from_filename("/home/krissemmy17/Exam-Project/spoti-data/2023_06_19_to_2023_06_26.csv")
        print(f"file successfully uploaded to Google Cloud Storage.")

    def run(self):
        self.perform_task()
        self.feature_eng()
        self.upload_to_storage()


job = Spotify_API()
job.run()
