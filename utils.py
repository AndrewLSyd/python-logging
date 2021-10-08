import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage
from google.cloud.exceptions import NotFound
import logging

def check_if_BQ_table_exists(table_id, bqclient=None, bqstorageclient=None):
    """
    Overview
        returns True or False depending on whether the table exists
    Arguments
        e.g. table_id = "wx-bq-poc.personal.AL_FBAA_MC_dacamp_prod_mc_final_crn_w_fb_2021-05-17_OSP-2373"
        NO tilde "`" surrounding table_id!
    """
    if bqclient is None:  # if a BQ client object is not passed through to the function
        # grab credentials from default login, use gcloud auth login
        credentials, your_project_id = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        # make clients
        bqclient = bigquery.Client(credentials=credentials, project='wx-bq-poc',)
        bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)   
    
    try:
        bqclient.get_table(table_id)  # Make an API request.
        logging.warning("Table {} already exists.".format(table_id))
        return True
    except NotFound:
        return False