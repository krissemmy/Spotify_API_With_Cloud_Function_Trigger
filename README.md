# Spotify_API_With_Cloud_Function_Trigger

## Spotify Data Collection and Feature Engineering
This repository contains Python scripts to collect recently played songs data from the Spotify API, perform feature engineering on the collected data, and upload the processed data to Google Cloud Storage. 

The project is divided into three main files:

- deploy.sh : A bash script to deploy a Google Cloud Function that will trigger the data collection and processing.

- main.py : Contains the main logic for data collection, feature engineering, and data upload to Google Cloud Storage.

- get_spotify_data.py : A script to test the functionality of main.py.

### How to Use
Follow the steps below to use this repository:

1. Set up a Google Cloud project and ensure you have the necessary credentials to access Google Cloud Storage.

2. Create a virtual environment and install the required dependencies by running the following command:
```
python -m venv my-venv
source my-venv/bin/activate
pip install -r requirements.txt
```
3. Set up the required environment variables in a .env file. Ensure to set the appropriate values for the Spotify API access (BASE64, REFRESH_TOKEN, EXPIRATION_TIME, ACCESS_TOKEN) and Google Cloud Storage (BUCKET_NAME).

4. Proceed to deploy the Google Cloud Function using the deploy.sh script. Ensure you have the Google Cloud SDK installed and authenticated.
```
./deploy.sh
```
The Google Cloud Function will be deployed, and it will automatically trigger the data collection and processing when a finalized object is uploaded to the specified Google Cloud Storage bucket.

5. Run the get_spotify_data.py script to test the data collection, feature engineering, and data upload processes.
```
python get_spotify_data.py
```

Note
This project is specifically designed to collect and process recently played songs data from the Spotify API. If you intend to use it for a different purpose, make necessary modifications to the code and environment variables accordingly.

Happy coding! 🚀




