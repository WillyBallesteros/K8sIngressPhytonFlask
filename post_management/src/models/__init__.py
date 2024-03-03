import os

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')
db_host = os.getenv('DB_HOST')

CONNECTION_STRING = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

k8spath = os.getenv('DELIVERY_DATABASE_URI')
if k8spath:
  CONNECTION_STRING = k8spath