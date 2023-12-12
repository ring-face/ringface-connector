from google.cloud import secretmanager
from google.oauth2 import service_account

import json
import logging
from decouple import config



def access_secret_version(project_id, secret_id, version_id="latest"):
    """
    Accesses the payload of the specified secret version.
    """

    logging.debug(f"Accessing the GSM at projects/{project_id}/secrets/{secret_id}/versions/{version_id}")
    client = gsm_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload

def gsm_client():
    credentials = service_account.Credentials.from_service_account_file(config("GCP_SA_JSON", default='./oauth-connector-sa.json'))
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    return client

def load_ring_auth_json():
    logging.info("Loading the ring auth file")

    project_id = config("GCP_PROJECT_ID")
    secret_id = config("RING_AUTH_SECRET_ID")
    secret_string = access_secret_version(project_id, secret_id)

    logging.debug(f"Secret projects/{project_id}/secrets/{secret_id} accessed successfully")

    config_data = json.loads(secret_string)
    return config_data

def add_secret_version(project_id, secret_id, new_secret_data):
    """
    Adds a new version to the specified secret with the given data.
    """
    client = gsm_client()
    parent = client.secret_path(project_id, secret_id)

    # Convert data to bytes
    payload = new_secret_data.encode("UTF-8")

    # Add the secret version
    response = client.add_secret_version(request={"parent": parent, "payload": {"data": payload}})
    return response

def update_ring_auth_json(token):

    logging.warn("UPDATING the ring auth file")


    project_id = config("GCP_PROJECT_ID")
    secret_id = config("RING_AUTH_SECRET_ID")

    # New secret data
    new_secret_data = json.dumps(token)

    # Add a new version
    response = add_secret_version(project_id, secret_id, new_secret_data)
    print(f"Added new secret version: {response.name}")