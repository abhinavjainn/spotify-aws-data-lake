# Data Lake on AWS ingested by Spotify APIs

![spotify_aws_data_lake_architecture](https://user-images.githubusercontent.com/71486660/160407208-4dd57233-0da3-4977-aeef-126e577cf00d.png)


This application collects data from [top 50 UK](https://open.spotify.com/playlist/37i9dQZEVXbMwmF30ppw50?si=701ed0ce8c234b69) and [top 50 global](https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=ad7071f3e7314f35) playlists from Spotify everyday.

Along with the songs, data are also collected on associated artists, albums, genre (hip hop, trance etc), track features (danceability, instrumentalness etc.), and spotify popularity index.

Application runs automatically everyday using AWS Lambda function triggered by Event Bridge and saves data in AWS S3.

Data collection is done to serve a broader scope and subsets can be used for specific analytical tasks.

AWS infrastructure is automated using Terraform.

Some possible use cases:
  - Analyse UK music trend against global one over a time period.
  - Draw insights on popular UK music preferences in a specific period or how it evolves over time.

[Sample of data in the lake](https://github.com/abhinavjainn/spotify-aws-data-lake/tree/main/sample-output)
