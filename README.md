# Ring connector module to download the data from the ring api

This ms will expose an endpoint to download the  `ding` events of the defined day (not the motion events), and save them in an mp4 file.
This video is ready for recognition.

## How to run
Install and run the python virtual env
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

You will need to define your .env file
```bash
ln -s ../ringface-db/data data # see the ringface-db project
cat <<EOF > print.sh > .env
DATA_DIR=./data
OAUTH_FILE=oauth-autorization.json
EOF
```
This file defines the location of the common database, and the location of the auth file created in the next step.


Next, you will need to fill the above referenced oauth token for accessing the ring api
```bash
./startCreateAuthFile.py
```
This will create the `oauth-autorization.json` file defined in the first step.


Now you can start the connector microservice. 
```bash
./startServer.sh
```
