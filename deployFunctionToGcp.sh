gcloud functions deploy downloadForToday \
--gen2 \
--runtime python310 \
--source=. \
--entry-point=downloadForToday \
--trigger-http \
--region=europe-west3 \
--allow-unauthenticated \
--env-vars-file .env.yaml
