gcloud functions deploy cloud-function \
--gen2 \
--region=us-central1 \
--runtime=python39 \
--memory=128Mi \
--entry-point=my_event \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=practice17" \
--trigger-location=us-central1