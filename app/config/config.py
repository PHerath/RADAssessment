import os

from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB_NAME = os.getenv('MYSQL_DB_NAME')
MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')


SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
