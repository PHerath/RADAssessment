import os

from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB_NAME = os.getenv('MYSQL_DB_NAME')
MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
