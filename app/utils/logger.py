import logging
import os


os.makedirs("logs", exist_ok=True)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")


index_logger = logging.getLogger("index")
index_logger.setLevel(logging.INFO)
index_handler = logging.FileHandler("logs/index.log", encoding="utf-8")
index_handler.setFormatter(formatter)
if not index_logger.handlers:
    index_logger.addHandler(index_handler)


query_logger = logging.getLogger("query")
query_logger.setLevel(logging.INFO)
query_handler = logging.FileHandler("logs/query.log", encoding="utf-8")
query_handler.setFormatter(formatter)
if not query_logger.handlers:
    query_logger.addHandler(query_handler)


error_logger = logging.getLogger("error")
error_logger.setLevel(logging.INFO)
error_handler = logging.FileHandler("logs/error.log", encoding="utf-8")
error_handler.setFormatter(formatter)
if not error_logger.handlers:
    error_logger.addHandler(error_handler)