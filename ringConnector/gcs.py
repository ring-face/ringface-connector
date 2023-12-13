import json
import logging
from google.cloud import storage
import io
from decouple import config


BUCKET_NAME = config("BUCKET_NAME")

def save_mp4_to_gcs(content, filename):
    """
    Save the MP4 content to a Google Cloud Storage bucket.

    :param content: The content of the MP4 file.
    :param filename: The filename to be used for the stored file.
    """

    # If content is a requests Response object, extract the content
    if hasattr(content, 'content'):
        content = content.content

    # Use a BytesIO wrapper for the content and upload it to GCS
    blob(filename).upload_from_file(io.BytesIO(content), content_type='video/mp4')

    logging.debug(f"File {filename} uploaded.")

def save_json_to_gcs(data, filename):

    # Convert the Python dictionary to JSON string
    if isinstance(data, dict):
        data = json.dumps(data)

    # Upload the JSON string to GCS
    blob(filename).upload_from_string(data, content_type='application/json')

    logging.debug(f"JSON file {filename} uploaded.")

def blob(filename):
    # Initialize a client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(BUCKET_NAME)

    # Create a blob (GCS file) in the bucket
    return bucket.blob(filename)
