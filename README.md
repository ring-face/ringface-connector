# Ring connector module to download the data from the ring api

This ms will expose an endpoint to download the  `ding` events of the defined day (not the motion events), and save them in an mp4 file.
This video is ready for recognition.

## How to run locally
Install and run the python virtual env
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Authentication
Ring uses a 2 factor authentication. You likley have your 2nd factor in your authentication app, like Microsoft or Google authenticator, already set up. Alternativaly, you use the sms 2nd factor. Either case, you will need to enter that 2nd factor after your password, to generate the `oauth-authorization.json` in the next step. 

```bash
./startCreateAuthFile.py
# enter your user, then password and then the 2nd factor from the Authorization app
```
This will create the `oauth-authorization.json` file defined in the first step in your current dir.

## Test your connection to your Ring device
Easiest, you can test your setup by downloading the videos of today from your Ring. 

You will need to define your .env file
```bash
ln -s ../ringface-db/data data # see the ringface-db project
cat <<EOF > print.sh > .env
DATA_DIR=./data # downoaded videos will end up here
OAUTH_FILE=oauth-authorization.json
EOF
```
This file defines the location of the common database, and the location of the auth file created in the previous step.

```bash
./startDownload.py # will download today
## or ./startDownload.py 2022-10-01 to download all the events from Oct 1, 2022
```
Check the downloaded videos in the `./data/videos` dir.

## Start the ms
Now you can now start the connector microservice. See https://github.com/ring-face/ringface for details.
```bash
./startServer.sh
```
