# gcp-sql-demo
Redis Enterprise as write-behind cache on GCP


### Deploy write-pubsub as Cloud Run Service to pick up keyspace notifications and send to a Google Cloud PubSub topic
```
pushd write-behind/write-pubsub

export GOOGLE_CLOUD_PROJECT=central-beach-194106

gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/write-pubsub

gcloud run deploy write-pubsub --image gcr.io/${GOOGLE_CLOUD_PROJECT}/write-pubsub \
--region=us-central1 \
--set-env-vars=GOOGLE_CLOUD_PROJECT=central-beach-194106,PUBSUB_TOPIC=glau-topic,\
REDIS_HOST=redis-14222.mc147-1.us-east1-mz.gcp.cloud.rlrcp.com,\
REDIS_PORT=14222,\
REDIS_PASSWORD=G9HxADlYc4ckq54fhxz5utv2fh8LxkB5

popd
```
   
### Deploy pubsub-sql on Google Cloud Function to pick up keyspace changes to a backend Cloud SQL 
```
pushd write-behind/pubsub-sql
gcloud functions deploy pubsub_sql --trigger-topic=glau-topic --region=us-central1  --runtime python310 
popd
```
