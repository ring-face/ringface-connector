gcloud functions deploy download-ring-video \
--gen2 \
--project ringface-2 \
--service-account connector-sa@ringface-2.iam.gserviceaccount.com \
--ingress-settings internal-and-gclb \
--runtime python310 \
--source=. \
--entry-point=download \
--trigger-http \
--region=europe-west3 \
--allow-unauthenticated \
--env-vars-file .env.yaml
