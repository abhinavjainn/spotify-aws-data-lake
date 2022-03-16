def file_header() -> list:
    header = ['snapshot_date',
              'snapshot_time',
              'snapshot_time_zone',
              'spotify_snapshot_id',
              'playlist_name',
              'followers_count',
              'playlist_tracks_count',
              'track_id',
              'track_name',
              'track_rank_in_playlist',
              'track_added_on',
              'track_spotify_popularity',
              'track_duration_ms',
              'album_name',
              'album_id',
              'album_type',
              'album_release_date',
              'tracks_in_album',
              'main_artist',
              'main_artist_id',
              'artist_genre',
              'danceability',
              'energy',
              'instrumentalness',
              'liveness',
              'loudness',
              'speechiness',
              'tempo'
              ]

    return header


def data_row() -> dict:
    row = {key: None for key in file_header()}
    return row
