gcloud functions deploy alpaca-shortcut \
--gen2 \
--runtime=python311 \
--region=us-central1 \
--source=. \
--entry-point=button_press \
--trigger-http \
--allow-unauthenticated