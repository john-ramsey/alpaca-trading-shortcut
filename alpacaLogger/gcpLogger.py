import logging
from google.cloud import logging as gcp_logging

client = gcp_logging.Client()
handler = client.get_default_handler()
cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(handler)
