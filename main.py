import functions_framework
from google.cloud import storage
from google.cloud import bigquery
import pandas as pd

storage_client = storage.Client()
bq_client = bigquery.Client()
table_id = "logical-craft-384210.alt.new_spotify_data"

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def my_event(cloud_event):
    data = cloud_event.data
    bucket_name = data.get("bucket")
    file_name = data.get("name")
    bucket = storage_client.bucket(bucket_name)
    
    # Extract the file from Google Cloud Storage
    blob = bucket.blob(file_name)
    with blob.open("r") as f:
        df = pd.read_csv(f)
        print(df.columns)

    # submit the job
    job = bq_client.load_table_from_dataframe(df, table_id)
    job.result()

    table = bq_client.get_table(table_id)
    print(f"Loaded {table.num_rows} and {len(table.schema)} into {table_id}")
