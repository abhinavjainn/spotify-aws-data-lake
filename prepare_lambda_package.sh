#!/usr/bin/env bash

# Copy Spotipy package to lambda package folder
cp -r venv/lib/python3.7/site-packages/spotipy lambda_package/

# Copy Requests package to lambda package folder
cp -r venv/lib/python3.7/site-packages/requests lambda_package/

# Copy config files to lambda package folder
mkdir lambda_package/config
cp config/playlists.py lambda_package/config/playlists.py
cp config/fileStructure.py lambda_package/config/fileStructure.py

# Copy main file to lambda package folder
cp app.py lambda_package/app.py

# Change working dir to lambda package folder
# shellcheck disable=SC2164
cd lambda_package/

# Zip contents of lambda package and save in main outer directory
# shellcheck disable=SC2035
zip -r ../lambda_package.zip *