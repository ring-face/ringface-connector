gcloud functions deploy download-ring-video \
--gen2 \
--service-account connector-sa@ringface-1.iam.gserviceaccount.com \
--runtime python310 \
--source=. \
--entry-point=download \
--trigger-http \
--region=europe-west3 \
--allow-unauthenticated \
--env-vars-file .env.yaml
