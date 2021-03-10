# Ring connector module to download the data from the ring api

First, you will need to define your .env file
```
cat <<EOF > print.sh > .env
DATA_DIR=./data
OAUTH_FILE=oauth-autorization.json
EOF
```
This file defines the location of the common database, and the location of the auth file created in the next step.


Next, you will need to get the oauth token for accessing the ring api
```bash
./startCreateAuthFile.py
```
This will create the `oauth-autorization.json` file defined in the first step.


Now you can download the events and its video for today. 
```bash
./startDownloadForToday.py
```
Will download the  `ding` events of today (not the motion events), and save them with the video.

This video is ready for recognition.