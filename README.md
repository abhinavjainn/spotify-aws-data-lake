# Data Lake on AWS ingested by Spotify APIs

This application collects data from top 50 UK and top 50 global playlists from Spotify everyday.

Along with the songs, data are also collected on associated artists, albums, genre (hip hop, trance etc), track features (danceability, instrumentalness etc.), and spotify popularity index.

Application runs automatically everyday using AWS Lambda function triggered by Event Bridge and saves data in AWS S3.

Data collection is done to serve a broader scope and subsets can be used for specific analytical tasks.

AWS infrastructure is automated using Terraform.

Some possible use cases:
  - Analyse UK music trend against global one over a time period.
  - Draw insights on popular UK music preferences in a specific period or how it evolves over time.
