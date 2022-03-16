import spotipy
import csv
import boto3
from config.playlists import playlist_ids
from config.fileStructure import file_header, data_row
from datetime import datetime, date
import time

spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())


def collect_data():
    for playlist, pid in playlist_ids().items():
        # Playlist header API
        playlist_header = spotify.playlist(pid)
        # Playlist items API
        playlist_items = spotify.playlist_items(pid)
        # Temporal fields
        datetime_now = datetime.now()
        date_now = date.today().strftime('%Y-%m-%d')
        time_now = datetime_now.strftime('%H:%M:%S')
        t_zone = time.tzname[0]
        year = datetime_now.year
        month = datetime_now.month
        day = datetime_now.day
        # Filenames
        filename = f"{playlist}_{date_now}_{time_now}.csv"
        tmp_file = f"/tmp/{filename}"

        # Process data and save in tmp file
        with open(tmp_file, 'w') as file:
            header = file_header()
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for idx, item in enumerate(playlist_items['items']):
                data = data_row()
                data['snapshot_date'] = date_now
                data['snapshot_time'] = time_now
                data['snapshot_time_zone'] = t_zone
                data['spotify_snapshot_id'] = playlist_header['snapshot_id']
                data['playlist_name'] = playlist_header['name']
                data['followers_count'] = playlist_header['followers']['total']
                data['playlist_tracks_count'] = playlist_items['total']
                data['track_id'] = item['track']['id']
                data['track_name'] = item['track']['name']
                data['track_rank_in_playlist'] = idx + 1
                data['track_added_on'] = item['added_at'][:10]
                data['track_spotify_popularity'] = item['track']['popularity']
                data['track_duration_ms'] = item['track']['duration_ms']
                data['album_name'] = item['track']['album']['name']
                data['album_id'] = item['track']['album']['id']
                data['album_type'] = item['track']['album']['album_type']
                data['album_release_date'] = item['track']['album']['release_date']
                data['tracks_in_album'] = item['track']['album']['total_tracks']
                data['main_artist'] = item['track']['album']['artists'][0]['name']
                data['main_artist_id'] = item['track']['album']['artists'][0]['id']
                # API call: Get artist details
                artist = spotify.artist(item['track']['album']['artists'][0]['id'])
                data['artist_genre'] = artist['genres'][0] if artist['genres'] else None
                # API call: Get audio features
                audio_features = spotify.audio_features(item['track']['id'])
                data['danceability'] = audio_features[0]['danceability']
                data['energy'] = audio_features[0]['energy']
                data['instrumentalness'] = audio_features[0]['instrumentalness']
                data['liveness'] = audio_features[0]['liveness']
                data['loudness'] = audio_features[0]['loudness']
                data['speechiness'] = audio_features[0]['speechiness']
                data['tempo'] = audio_features[0]['tempo']
                writer.writerow(data)

        # Save data in AWS S3 bucket (spotify-data-lake)
        aws_s3 = boto3.resource('s3')
        aws_file = f'{year}/{month}/{day}/{filename}'
        aws_s3.Object('spotify-data-lake', aws_file).upload_file(tmp_file)


def lambda_handler(event, context):
    collect_data()


if __name__ == "__main__":
    collect_data()
