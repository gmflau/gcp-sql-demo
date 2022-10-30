# Copyright 2022 Redis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_pubsub_publish]
import base64
import json
import os
import redis
import sqlalchemy
import process_hash
import process_del
from google.cloud import pubsub_v1


# Initialize Redis connection
redis_host = os.environ['REDIS_HOST']
redis_port = os.environ['REDIS_PORT']
redis_password = os.environ['REDIS_PASSWORD']
redis_client = redis.StrictRedis(host=redis_host, port=redis_port,
                   password=redis_password, decode_responses=True)

# Initialize PostgreSQL DB connection parameters
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
table_name = "car_dealers"
table_field = "id,make,model,year,state"
driver_name = 'postgres+pg8000'
query_string =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(db_connection_name)})


# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()


# Create SQLAlchemy Engine
db = sqlalchemy.create_engine(
       sqlalchemy.engine.url.URL(
         drivername=driver_name,
         username=db_user,
         password=db_password,
         database=db_name,
         query=query_string,
       ),
       pool_size=5,
       max_overflow=2,
       pool_timeout=30,
       pool_recycle=1800
     )

# Triggered from a message on a Cloud Pub/Sub topic.
def pubsub_sql(event, context):
    # Print out the data from Pub/Sub, to prove that it worked
    #print(event['data'])
    print("Message from PubSub - Topic: glau-topic")
    message = base64.b64decode(event['data'])
    print(message)
    msg_json=json.loads(message.decode('utf-8'))
    print(msg_json['data']['message']['data'])
    operation=msg_json['data']['message']['data']
    print('** operation => {}'.format(operation))

    match operation:
        case 'hset':
            print("This operation is hset")
            process_hash.hset(db, redis_client, msg_json)
        case 'set':
            print("This operation is set")
        case 'del':
            print("This operation is del")
            process_del.execute(db, msg_json)
        case other:
            print("No match found")    

