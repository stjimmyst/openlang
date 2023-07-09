import logging
import google.cloud.logging


OL_logger = logging
client = google.cloud.logging.Client()
client.setup_logging(log_level=logging.DEBUG)

print("Logger initialised")

def RequestLog(route, body):
    OL_logger.debug("RequestRoute", extra={"route":route,"body": "body"})