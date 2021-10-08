"""
logging example 1 - a bit more functionality
"""
import logging

import os

import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage

import utils

##################################################
# SET UP LOGGER
##################################################
# root logger
logger = logging.getLogger()  # default level of logger is WARNING and above
logger.setLevel(logging.DEBUG)  # need to set root logger to the lowest level

# create file handler which logs even debug messages
file_handler = logging.FileHandler('log.txt')
file_handler.setLevel(logging.DEBUG)

# add console handler
console_handler = logging.StreamHandler()  # console handler
console_handler.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s | %(filename)s | function: %(funcName)s | line: %(lineno)d : %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

##################################################
# MAIN
##################################################
BQ_TABLE = "digital_attribution_modelling"
BQ_PROJECT = "wx-bq-poc"
FW = '2021-09-27'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "adc.json" 
os.environ['GOOGLE_CLOUD_PROJECT'] = "wx-bq-poc"
logging.info("os.environ['GOOGLE_CLOUD_PROJECT'] = " + str(os.environ['GOOGLE_CLOUD_PROJECT']))

# grab credentials from default login, use gcloud auth login
credentials, your_project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Make clients.
bqclient = bigquery.Client(credentials=credentials, project=BQ_PROJECT,)
bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)

logging.info("bqclients and bqstorage clients instantiated")

if utils.check_if_BQ_table_exists("wx-bq-poc.personal.AL_tmp_inc_sales_{fw_no_dash}".format(fw_no_dash=FW[:4] + FW[5:7] + FW[-2:])):
    logging.warning("rerunning")

query_string = """
CREATE OR REPLACE TABLE
  `wx-bq-poc.personal.AL_tmp_inc_sales_{fw_no_dash}` AS (
  SELECT
    fw_start_date,
    campaign_code,
    campaign_start_date,
    COUNT(DISTINCT crn) AS distinct_crn,
    SUM(inc_sales) AS inc_sales
  FROM
    `Attribution_Safari_GT_output.Safari_crn_level_game_theory_output_safari_full_promo_halo_post_current`
  WHERE
    pph = 'promo'
    AND fw_start_date = '{fw}'
  GROUP BY
    1,
    2,
    3
  ORDER BY
    1,
    2,
    3 );
""".format(fw=FW, fw_no_dash=FW[:4] + FW[5:7] + FW[-2:])

logging.debug(str(query_string))

# df_bq = (
# bqclient.query(query_string)
# .result()
# .to_dataframe(bqstorage_client=bqstorageclient)
# )

logging.info("all done")
